"""
Theil–Sen Robust Trend Slope Estimator & Confidence Intervals
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Mathematical Formulation:
- Slope beta: Median of all pairwise slopes:
    beta = median({ (y_j - y_i) / (x_j - x_i) : 1 <= i < j <= n })
- Intercept alpha:
    alpha = median(y_i - beta * x_i)
- Non-parametric rank-based confidence interval (Gilbert 1987 / Sen 1968):
    N' = n * (n - 1) / 2
    C_alpha = Z_{1 - alpha/2} * sqrt(Var(S))
    M1 = int((N' - C_alpha) / 2)
    M2 = int((N' + C_alpha) / 2) + 1
    CI_lower = slopes_sorted[M1]
    CI_upper = slopes_sorted[M2]
- Decadal rate of change: beta * 10
- Percent change over observation window: (beta * total_years / mean_y) * 100%
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np
from scipy import stats


def theil_sen_estimator(
    y: Union[List[float], np.ndarray],
    x: Optional[Union[List[float], np.ndarray]] = None,
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Compute Theil-Sen robust slope estimator with non-parametric confidence intervals.
    """
    y_arr = np.asarray(y, dtype=float)
    if x is None:
        x_arr = np.arange(len(y_arr), dtype=float)
    else:
        x_arr = np.asarray(x, dtype=float)

    # Filter out missing/NaN values
    valid_mask = (~np.isnan(y_arr)) & (~np.isnan(x_arr))
    y_clean = y_arr[valid_mask]
    x_clean = x_arr[valid_mask]
    n = len(y_clean)

    if n < 4:
        return {
            "n_observations": n,
            "slope": 0.0,
            "slope_decadal": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "intercept": 0.0,
            "pct_change_total": 0.0,
            "mean_value": float(np.mean(y_clean)) if n > 0 else 0.0,
            "alpha": alpha
        }

    # Pairwise slopes
    slopes = []
    for i in range(n - 1):
        dx = x_clean[i + 1:] - x_clean[i]
        dy = y_clean[i + 1:] - y_clean[i]
        non_zero = dx != 0
        if np.any(non_zero):
            pairwise = dy[non_zero] / dx[non_zero]
            slopes.extend(pairwise.tolist())

    if len(slopes) == 0:
        return {
            "n_observations": n,
            "slope": 0.0,
            "slope_decadal": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "intercept": float(np.median(y_clean)),
            "pct_change_total": 0.0,
            "mean_value": float(np.mean(y_clean)),
            "alpha": alpha
        }

    slopes.sort()
    n_slopes = len(slopes)
    median_slope = float(np.median(slopes))

    # Intercept alpha = median(y - beta * x)
    intercept = float(np.median(y_clean - median_slope * x_clean))

    # Calculate Kendall's Var(S) for confidence interval bounds
    unique_vals, counts = np.unique(y_clean, return_counts=True)
    ties = counts[counts > 1]
    tie_term = np.sum(ties * (ties - 1) * (2 * ties + 5))
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0

    z_crit = stats.norm.ppf(1.0 - alpha / 2.0)
    c_alpha = z_crit * np.sqrt(var_s)

    m1 = max(0, int((n_slopes - c_alpha) / 2.0))
    m2 = min(n_slopes - 1, int((n_slopes + c_alpha) / 2.0))

    ci_lower = float(slopes[m1])
    ci_upper = float(slopes[m2])

    # Percentage change
    mean_val = float(np.mean(y_clean))
    total_span_years = float(x_clean.max() - x_clean.min())
    if abs(mean_val) > 1e-6 and total_span_years > 0:
        pct_change = (median_slope * total_span_years / mean_val) * 100.0
    else:
        pct_change = 0.0

    return {
        "n_observations": int(n),
        "slope": round(median_slope, 4),
        "slope_decadal": round(median_slope * 10.0, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "intercept": round(intercept, 4),
        "pct_change_total": round(pct_change, 2),
        "mean_value": round(mean_val, 4),
        "alpha": alpha
    }
