"""
Unit Tests for Statistical Methodology: Mann-Kendall, Theil-Sen, FDR
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
"""

import pytest
import numpy as np

from src.statistics.mann_kendall import mann_kendall_test
from src.statistics.theil_sen import theil_sen_estimator
from src.statistics.autocorrelation import assess_autocorrelation
from src.statistics.fdr_correction import benjamini_hochberg_correction


def test_mann_kendall_increasing_trend():
    """Verify Mann-Kendall correctly detects strictly increasing monotonic trend."""
    x = np.arange(1, 25, dtype=float) # 1, 2, 3, ..., 24
    res = mann_kendall_test(x)
    assert res["trend"] == "Increasing"
    assert res["is_significant"] is True
    assert res["z_statistic"] > 3.0
    assert res["p_value"] < 0.001
    assert pytest.approx(res["kendalls_tau"], 0.001) == 1.0


def test_mann_kendall_decreasing_trend():
    """Verify Mann-Kendall correctly detects strictly decreasing monotonic trend."""
    x = np.arange(25, 1, -1, dtype=float)
    res = mann_kendall_test(x)
    assert res["trend"] == "Decreasing"
    assert res["is_significant"] is True
    assert res["z_statistic"] < -3.0
    assert res["p_value"] < 0.001
    assert pytest.approx(res["kendalls_tau"], 0.001) == -1.0


def test_mann_kendall_no_trend():
    """Verify Mann-Kendall returns No Significant Trend for constant series."""
    x = np.full(20, 50.0)
    res = mann_kendall_test(x)
    assert res["trend"] == "No Significant Trend"
    assert res["is_significant"] is False
    assert res["s_statistic"] == 0.0
    assert res["p_value"] == 1.0


def test_theil_sen_known_slope():
    """Verify Theil-Sen recovers exact known linear slope."""
    x = np.arange(20, dtype=float)
    # y = 2.5 * x + 10.0 + slight noise
    y = 2.5 * x + 10.0
    res = theil_sen_estimator(y, x)
    assert pytest.approx(res["slope"], 0.01) == 2.5
    assert pytest.approx(res["intercept"], 0.01) == 10.0
    assert res["ci_lower"] <= res["slope"] <= res["ci_upper"]


def test_autocorrelation_white_noise_vs_ar1():
    """Verify lag-1 autocorrelation detects correlated series."""
    np.random.seed(42)
    white_noise = np.random.normal(0, 1, 50)
    res_white = assess_autocorrelation(white_noise)
    assert res_white["is_significant"] is False

    # AR(1) process with phi = 0.85
    ar1 = np.zeros(60)
    for t in range(1, 60):
        ar1[t] = 0.85 * ar1[t-1] + np.random.normal(0, 1)
    res_ar1 = assess_autocorrelation(ar1)
    assert res_ar1["is_significant"] is True
    assert res_ar1["lag1_autocorr"] > 0.5


def test_benjamini_hochberg_fdr():
    """Verify Benjamini-Hochberg FDR q-value adjustment."""
    test_records = [
        {"p_value": 0.001, "district": "D1"},
        {"p_value": 0.008, "district": "D2"},
        {"p_value": 0.039, "district": "D3"}, # marginal
        {"p_value": 0.450, "district": "D4"},
        {"p_value": 0.820, "district": "D5"}
    ]
    adjusted = benjamini_hochberg_correction(test_records, alpha=0.05)
    
    assert len(adjusted) == 5
    # The lowest p-value should remain significant after FDR
    assert adjusted[0]["significance_class"] == "Statistically Significant (FDR-Controlled)"
    assert adjusted[0]["q_value"] < 0.05
    # The high p-values should be marked insignificant
    assert adjusted[3]["significance_class"] == "Statistically Insignificant"
    assert adjusted[4]["significance_class"] == "Statistically Insignificant"
