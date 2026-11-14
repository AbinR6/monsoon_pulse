"""
Unit Tests for Scientific Indicators: R95p, HMV, RTE
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
"""

import pytest
import numpy as np
import pandas as pd

from src.science.r95p_calculator import R95pCalculator
from src.science.hmv_calculator import HmvCalculator
from src.science.rte_calculator import RteCalculator


def test_r95p_calculation_synthetic_benchmark():
    """
    Test ETCCDI R95p on a known controlled synthetic precipitation series.
    """
    dates = pd.date_range("2010-01-01", "2010-12-31", freq="D")
    n = len(dates)
    
    # 265 dry days (0.0), 90 moderate wet days (10 mm), 10 extreme days (50 to 140 mm)
    precip = np.zeros(n)
    precip[50:140] = 10.0 # 90 days of 10mm
    for idx, rain in enumerate(range(50, 150, 10)): # 10 days: 50, 60, 70, 80, 90, 100, 110, 120, 130, 140 mm
        precip[200 + idx] = float(rain)

    df_synth = pd.DataFrame({
        "date": dates,
        "year": dates.year,
        "month": dates.month,
        "district": "TestDistrict",
        "precipitation_mm": precip
    })

    calc = R95pCalculator(wet_day_threshold_mm=1.0, baseline_period=(2010, 2010))
    p95 = calc.compute_district_threshold(df_synth)
    
    # Total wet days = 100. 95th percentile falls at the 95th value (approx 100 mm).
    assert 10.0 < p95 < 140.0

    annual_res = calc.calculate_annual_r95p(df_synth, threshold_p95=p95)
    row = annual_res.iloc[0]
    
    # Extreme days (> p95) should be non-zero and r95p_annual > 0
    assert row["extreme_days_count"] > 0
    assert row["r95p_annual_mm"] > 0
    assert row["wet_days_count"] == 100
    assert row["rx1day_mm"] == 140.0


def test_hmv_calculation_synthetic_benchmark():
    """
    Test HMV formula: HMV = (Z_LST - Z_SMAP - Z_NDVI) / 3.
    """
    years = [2015, 2016, 2017, 2018, 2019, 2020]
    dist = "TestDistrict"

    # Year 2016: extreme heat, low soil moisture, low NDVI -> High Positive HMV (Thermal Stress)
    df_lst = pd.DataFrame({
        "district": [dist]*6,
        "year": years,
        "lst_mean_celsius": [30.0, 35.0, 30.0, 30.0, 30.0, 30.0]
    })
    df_smap = pd.DataFrame({
        "district": [dist]*6,
        "year": years,
        "sm_mean_m3_m3": [0.30, 0.15, 0.30, 0.30, 0.30, 0.30]
    })
    df_ndvi = pd.DataFrame({
        "district": [dist]*6,
        "year": years,
        "ndvi_mean": [0.70, 0.50, 0.70, 0.70, 0.70, 0.70]
    })

    hmv_calc = HmvCalculator(baseline_period=(2015, 2020))
    res = hmv_calc.calculate_hmv(df_lst, df_smap, df_ndvi, [dist])

    row_2016 = res[res["year"] == 2016].iloc[0]
    # In 2016: Z_LST > 0, Z_SMAP < 0, Z_NDVI < 0
    # Therefore Z_LST - Z_SMAP - Z_NDVI must be strongly positive
    assert row_2016["z_lst"] > 1.0
    assert row_2016["z_smap"] < -1.0
    assert row_2016["z_ndvi"] < -1.0
    assert row_2016["hmv"] > 1.0
    assert "Stress" in row_2016["condition"]


def test_rte_calculation_synthetic_benchmark():
    """
    Test RTE formula: RTE = Z_R95p,JJAS * S_norm.
    """
    terrain = {
        "SteepDist": {"normalized_slope": 1.0, "mean_slope_deg": 25.0, "p90_slope_deg": 40.0, "mean_elevation_m": 800.0},
        "FlatDist": {"normalized_slope": 0.0, "mean_slope_deg": 1.0, "p90_slope_deg": 2.0, "mean_elevation_m": 10.0}
    }

    df_r95p = pd.DataFrame({
        "district": ["SteepDist", "SteepDist", "FlatDist", "FlatDist"],
        "year": [2017, 2018, 2017, 2018],
        "r95p_jjas_mm": [500.0, 1500.0, 500.0, 1500.0]
    })

    rte_calc = RteCalculator(terrain)
    res = rte_calc.calculate_rte(df_r95p)

    # In 2018 (extreme year, Z_R95p > 0):
    # SteepDist (S_norm = 1.0) has high positive RTE
    # FlatDist (S_norm = 0.0) has RTE = 0.0 regardless of rainfall!
    row_steep_2018 = res[(res["district"] == "SteepDist") & (res["year"] == 2018)].iloc[0]
    row_flat_2018 = res[(res["district"] == "FlatDist") & (res["year"] == 2018)].iloc[0]

    assert row_steep_2018["rte"] > 0.5
    assert pytest.approx(row_flat_2018["rte"], 0.001) == 0.0
    assert row_steep_2018["terrain_contribution"] == 1.0
    assert row_flat_2018["terrain_contribution"] == 0.0
