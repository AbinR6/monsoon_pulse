"""
Unit Tests for Statistical Methodology: Mann-Kendall, Theil-Sen, FDR, Yue-Wang
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


def test_yue_wang_variance_correction_inflates_variance():
    """Verify full Yue & Wang (2004) variance correction factor inflates Var(S)."""
    np.random.seed(123)
    n = 30
    # Create serially correlated trended series
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.7 * x[t-1] + np.random.normal(0, 1) + 0.3 * t

    autocorr = assess_autocorrelation(x)
    eta = autocorr["variance_correction_factor_eta"]
    assert eta >= 1.0

    mk_standard = mann_kendall_test(x, modified_for_autocorr=False)
    mk_modified = mann_kendall_test(x, modified_for_autocorr=True, variance_correction_factor_eta=eta)

    assert mk_modified["var_s_star"] >= mk_standard["var_s"]
    assert abs(mk_modified["z_statistic"]) <= abs(mk_standard["z_statistic"])


def test_theil_sen_consistent_ci_with_modified_variance():
    """Verify Theil-Sen confidence intervals widen consistently when Var*(S) is inflated."""
    x = np.arange(24, dtype=float)
    y = 0.5 * x + np.random.normal(0, 1, 24)

    # Standard uncorrected CI
    res_std = theil_sen_estimator(y, x)
    width_std = res_std["ci_upper"] - res_std["ci_lower"]

    # Modified inflated variance CI (e.g. eta = 1.8)
    var_s_inflated = res_std["var_s_used"] * 1.8
    res_mod = theil_sen_estimator(y, x, var_s_override=var_s_inflated)
    width_mod = res_mod["ci_upper"] - res_mod["ci_lower"]

    # When variance of S is inflated, the rank bounds widen
    assert width_mod >= width_std


def test_benjamini_hochberg_fdr():
    """Verify Benjamini-Hochberg FDR q-value adjustment."""
    test_records = [
        {"p_value": 0.001, "district": "D1"},
        {"p_value": 0.008, "district": "D2"},
        {"p_value": 0.039, "district": "D3"},
        {"p_value": 0.450, "district": "D4"},
        {"p_value": 0.820, "district": "D5"}
    ]
    adjusted = benjamini_hochberg_correction(test_records, alpha=0.05)
    
    assert len(adjusted) == 5
    assert adjusted[0]["significance_class"] == "Statistically Significant (FDR-Controlled)"
    assert adjusted[0]["q_value"] < 0.05
    assert adjusted[3]["significance_class"] == "Statistically Insignificant"
    assert adjusted[4]["significance_class"] == "Statistically Insignificant"
