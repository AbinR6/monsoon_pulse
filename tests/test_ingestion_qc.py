"""
Unit Tests for Ingestion, Units Conversion & Quality Control
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
"""

import pytest
import numpy as np
import pandas as pd

from src.ingestion.boundary_reader import load_districts, get_district_list, get_district_metadata
from src.ingestion.units_converter import kelvin_to_celsius, scale_modis_lst, scale_ndvi, mm_per_hr_to_daily_sum, normalize_slope
from src.ingestion.quality_control import QualityAssuranceValidator, PHYSICAL_BOUNDS


def test_district_boundaries_load_14_districts():
    """Verify that exactly 14 official Kerala districts are loaded."""
    districts = get_district_list()
    assert len(districts) == 14
    expected_districts = [
        "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam",
        "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta",
        "Thiruvananthapuram", "Thrissur", "Wayanad"
    ]
    assert sorted(districts) == sorted(expected_districts)


def test_district_metadata_integrity():
    """Verify metadata contains required physiographic zones and positive areas."""
    meta = get_district_metadata()
    assert len(meta) == 14
    for dist, props in meta.items():
        assert "zone" in props
        assert props["area_sq_km"] > 0
        assert props["mean_elevation_m"] >= 0
        assert props["mean_slope_deg"] >= 0


def test_units_conversion_kelvin_to_celsius():
    """Verify Kelvin to Celsius conversion formula."""
    assert pytest.approx(kelvin_to_celsius(273.15), 0.01) == 0.0
    assert pytest.approx(kelvin_to_celsius(300.0), 0.01) == 26.85
    assert pytest.approx(kelvin_to_celsius(310.15), 0.01) == 37.0


def test_scale_modis_lst():
    """Verify MODIS LST digital number scaling (0.02) and Celsius conversion."""
    # Raw DN = 15000 -> 15000 * 0.02 = 300 K -> 26.85 C
    celsius = scale_modis_lst(15000)
    assert pytest.approx(celsius, 0.01) == 26.85


def test_scale_ndvi():
    """Verify MODIS NDVI scaling factor 0.0001."""
    # Raw DN = 7500 -> 0.75
    ndvi = scale_ndvi(7500)
    assert pytest.approx(ndvi, 0.0001) == 0.75
    # Negative value: -1000 -> -0.1
    assert pytest.approx(scale_ndvi(-1000), 0.0001) == -0.1


def test_precipitation_rate_integration():
    """Verify integration of 48 half-hourly intervals to daily mm sum."""
    rates = np.full(48, 10.0) # 10 mm/hr for 24 hours
    daily_sum = mm_per_hr_to_daily_sum(rates, interval_hours=0.5)
    assert pytest.approx(daily_sum, 0.01) == 240.0


def test_normalize_slope():
    """Verify min-max normalization of terrain slope."""
    norm = normalize_slope(slope_deg=10.0, min_slope=0.0, max_slope=20.0)
    assert pytest.approx(norm, 0.001) == 0.5
    assert pytest.approx(normalize_slope(0.0, 0.0, 20.0), 0.001) == 0.0
    assert pytest.approx(normalize_slope(20.0, 0.0, 20.0), 0.001) == 1.0


def test_quality_control_physical_bounds():
    """Verify QA validator detects physical boundary violations."""
    # Valid temperatures
    valid_lst = pd.Series([25.0, 28.5, 33.2, 38.0])
    res_valid = QualityAssuranceValidator.validate_series(valid_lst, "lst_celsius")
    assert res_valid["is_valid"] is True
    assert res_valid["out_of_bounds_high"] == 0

    # Out of bounds temperature (e.g. 75 C is impossible for land in Kerala)
    invalid_lst = pd.Series([25.0, 75.0, -10.0])
    res_invalid = QualityAssuranceValidator.validate_series(invalid_lst, "lst_celsius")
    assert res_invalid["is_valid"] is False
    assert res_invalid["out_of_bounds_high"] == 1
    assert res_invalid["out_of_bounds_low"] == 1


def test_missing_values_tracked_not_zero_filled():
    """Verify that missing observations are tracked and not silently zero-filled."""
    series_with_nans = pd.Series([25.0, np.nan, 30.0, np.nan])
    res = QualityAssuranceValidator.validate_series(series_with_nans, "lst_celsius", allow_nan=True)
    assert res["missing_records"] == 2
    assert res["valid_records"] == 2
    assert res["completeness_pct"] == 50.0
