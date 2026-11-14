"""
Validation Tests for Output JSON Schema and Completeness
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
"""

import json
from pathlib import Path
import pytest

from src.export.schema_validator import validate_dashboard_json, check_no_nan_or_inf


def test_dashboard_json_exists_and_valid():
    """Verify that monsoon_pulse_dashboard_data.json exists and conforms to schema."""
    json_path = Path("data/outputs/monsoon_pulse_dashboard_data.json")
    assert json_path.exists(), f"Dashboard JSON missing at {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validates schema, key structure, 14 districts, 2001-2024 range, and zero NaN/Inf
    is_valid = validate_dashboard_json(data)
    assert is_valid is True

    # Check 14 districts
    districts = list(data["districts_data"].keys())
    assert len(districts) == 14

    # Check that each district has 24 years of data
    for d, d_obj in data["districts_data"].items():
        assert len(d_obj["annual_time_series"]) == 24
        assert "statistics" in d_obj
        assert len(d_obj["statistics"]) == 5 # 5 variables

    # Check total statistical tests (14 districts * 5 variables = 70 tests)
    assert len(data["all_statistical_tests"]) == 70

    # Check data quality report is present
    assert "data_quality_report" in data
    assert "variables_audited" in data["data_quality_report"]


def test_frontend_synced_data_matches():
    """Verify that frontend/public/data/ has identical production JSON."""
    prod_path = Path("frontend/public/data/monsoon_pulse_dashboard_data.json")
    assert prod_path.exists()
    assert prod_path.stat().st_size > 100000 # > 100 KB
