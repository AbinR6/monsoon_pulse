"""
Autocorrelation and Serial Dependency Assessment Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Methodology conforms to Yue & Wang (2004) and Anderson (1942):
- Trend-Free Pre-Whitening / Residual Autocorrelation:
    Evaluates autocorrelation on detrended residuals e_t = x_t - (alpha + beta * t)
    to prevent conflating a genuine physical trend with serial autocorrelation.
- Sample Autocorrelation Function (ACF):
    r_k = sum_{t=1}^{n-k} (e_t - e_bar)(e_{t+k} - e_bar) / sum_{t=1}^n (e_t - e_bar)^2
- Anderson 95% Two-Tailed Confidence Limits for white noise:
    CI = (-1 +- 1.96 * sqrt(n - k - 1)) / (n - k)
- Yue & Wang (2004) Variance Correction Factor (eta):
    eta = 1 + [ 2 / (n(n-1)(n-2)) ] * sum_{k=1}^{n-1} (n - k)(n - k - 1)(n - k - 2) * r_k
    where significant r_k are retained to calculate the effective sample size inflation factor.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np


def compute_sample_acf(residuals: np.ndarray, max_lag: Optional[int] = None) -> np.ndarray:
    """
    Compute sample autocorrelation function r_k for lags k = 0, ..., max_lag.
    """
    n = len(residuals)
    if max_lag is None:
        max_lag = n - 1
    max_lag = min(max_lag, n - 1)

    mean_res = np.mean(residuals)
    diff = residuals - mean_res
    variance = np.sum(diff ** 2)

    if variance < 1e-12:
        return np.zeros(max_lag + 1)

    acf = np.zeros(max_lag + 1)
    acf[0] = 1.0

    for k in range(1, max_lag + 1):
        acf[k] = np.sum(diff[:-k] * diff[k:]) / variance

    return acf


def assess_autocorrelation(
    x: Union[List[float], np.ndarray], 
    alpha: float = 0.05,
    theil_sen_slope: Optional[float] = None
) -> Dict[str, Any]:
    """
    Compute lag-1 and multi-lag serial autocorrelation.
    If theil_sen_slope is provided (or estimated), evaluates autocorrelation on
    trend-free residuals (Yue & Wang 2004).
    """
    arr = np.asarray(x, dtype=float)
    clean_indices = np.where(~np.isnan(arr))[0]
    clean_vals = arr[clean_indices]
    n = len(clean_vals)

    if n < 5:
        return {
            "n_observations": n,
            "lag1_autocorr": 0.0,
            "lag1_raw": 0.0,
            "anderson_lower": -1.0,
            "anderson_upper": 1.0,
            "is_significant": False,
            "significant_lags": [],
            "variance_correction_factor_eta": 1.0,
            "recommendation": "Standard Mann-Kendall"
        }

    # Raw lag-1 autocorrelation
    mean_raw = np.mean(clean_vals)
    diff_raw = clean_vals - mean_raw
    denom_raw = np.sum(diff_raw ** 2)
    lag1_raw = float(np.sum(diff_raw[:-1] * diff_raw[1:]) / denom_raw) if denom_raw > 1e-12 else 0.0

    # Trend removal for Yue & Wang procedure
    if theil_sen_slope is None:
        # Estimate median pairwise slope
        pairwise = []
        for i in range(n - 1):
            dx = clean_indices[i + 1:] - clean_indices[i]
            dy = clean_vals[i + 1:] - clean_vals[i]
            pairwise.extend((dy / dx).tolist())
        theil_sen_slope = float(np.median(pairwise)) if len(pairwise) > 0 else 0.0

    residuals = clean_vals - theil_sen_slope * clean_indices
    acf = compute_sample_acf(residuals, max_lag=n - 1)
    lag1_detrended = float(acf[1]) if len(acf) > 1 else 0.0

    # Anderson 95% critical bounds for lag 1
    z_crit = 1.96
    lower_bound_lag1 = (-1.0 - z_crit * np.sqrt(n - 2)) / (n - 1)
    upper_bound_lag1 = (-1.0 + z_crit * np.sqrt(n - 2)) / (n - 1)

    # Multi-lag significance and Yue & Wang variance correction factor (eta)
    significant_lags = []
    eta_sum = 0.0

    for k in range(1, n - 2):
        r_k = acf[k]
        # Anderson test for lag k
        ci_lower = (-1.0 - z_crit * np.sqrt(n - k - 1)) / (n - k)
        ci_upper = (-1.0 + z_crit * np.sqrt(n - k - 1)) / (n - k)

        if r_k < ci_lower or r_k > ci_upper:
            significant_lags.append(int(k))
            weight = (n - k) * (n - k - 1) * (n - k - 2)
            eta_sum += weight * r_k

    # Full Yue & Wang (2004) variance factor
    # eta = 1 + [ 2 / (n(n-1)(n-2)) ] * sum_{k=1}^{n-1} (n - k)(n - k - 1)(n - k - 2) * r_k
    denom_eta = n * (n - 1) * (n - 2)
    eta = 1.0 + (2.0 / denom_eta) * eta_sum if denom_eta > 0 else 1.0

    # Eta is bounded below by 1.0 (variance is not deflated for positive autocorrelation)
    eta = max(1.0, float(eta))

    is_significant = (1 in significant_lags) or (lag1_detrended < lower_bound_lag1) or (lag1_detrended > upper_bound_lag1)
    recommendation = "Modified Mann-Kendall (Yue & Wang 2004)" if is_significant else "Standard Mann-Kendall"

    return {
        "n_observations": int(n),
        "lag1_autocorr": round(lag1_detrended, 4),
        "lag1_raw": round(lag1_raw, 4),
        "anderson_lower": round(float(lower_bound_lag1), 4),
        "anderson_upper": round(float(upper_bound_lag1), 4),
        "is_significant": bool(is_significant),
        "significant_lags": significant_lags,
        "variance_correction_factor_eta": round(eta, 4),
        "recommendation": recommendation
    }
