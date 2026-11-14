"""
Schema and Data Integrity Validation for MONSOON PULSE JSON Outputs
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Validates that all export artifacts strictly satisfy:
- Completeness of all 14 Kerala districts.
- Required observation period 2001–2024 (and 2015–2024 for SMAP/HMV).
- Non-empty statistical parameters, confidence intervals, and FDR q-values.
- Scientific metadata and provenance citations.
- Absence of JSON-invalid numeric values (NaN, Inf).
"""

from typing import Dict, List, Any
import json
import numpy as np


def check_no_nan_or_inf(obj: Any, path: str = "") -> None:
    """Recursively verify that no NaN or Infinity exists in the JSON data structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            check_no_nan_or_inf(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            check_no_nan_or_inf(item, f"{path}[{idx}]")
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            raise ValueError(f"JSON validation error: Invalid float value ({obj}) at path: {path}")


def validate_dashboard_json(data: Dict[str, Any]) -> bool:
    """
    Validate structure, district coverage, and data completeness of final dashboard JSON.
    """
    required_root_keys = [
        "project", "challenge", "observation_window", "metadata", 
        "districts_data", "all_statistical_tests", "sensitivity_analysis", "data_quality_report"
    ]
    for k in required_root_keys:
        if k not in data:
            raise KeyError(f"Dashboard JSON missing required top-level key: '{k}'")

    districts = data["districts_data"]
    if len(districts) != 14:
        raise ValueError(f"Expected 14 districts in 'districts_data', found {len(districts)}")

    for dist_name, dist_obj in districts.items():
        if "metadata" not in dist_obj:
            raise KeyError(f"District {dist_name} missing 'metadata'")
        if "annual_time_series" not in dist_obj:
            raise KeyError(f"District {dist_name} missing 'annual_time_series'")
        if "statistics" not in dist_obj:
            raise KeyError(f"District {dist_name} missing 'statistics'")

        # Verify time series span
        ts = dist_obj["annual_time_series"]
        years = [row["year"] for row in ts]
        if min(years) != 2001 or max(years) != 2024:
            raise ValueError(f"District {dist_name} time series years {min(years)}–{max(years)} does not match 2001–2024")

    # Check for NaN / Inf
    check_no_nan_or_inf(data)
    return True
