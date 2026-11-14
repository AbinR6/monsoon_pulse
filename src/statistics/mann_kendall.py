"""
Mann–Kendall Non-Parametric Trend Testing Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Mathematical Formulation:
- Kendall's S statistic:
    S = sum_{i=1}^{n-1} sum_{j=i+1}^n sgn(x_j - x_i)
- Variance with tie correction:
    Var(S) = (1/18) * [ n(n-1)(2n+5) - sum_t t(t-1)(2t+5) ]
- Standardized test statistic Z:
    Z = (S - 1) / sqrt(Var(S))   if S > 0
    Z = 0                        if S == 0
    Z = (S + 1) / sqrt(Var(S))   if S < 0
- Two-tailed p-value:
    p = 2 * (1 - Phi(|Z|))
- Includes Modified Mann-Kendall variance correction for serial correlation (Yue & Wang / Hamed & Rao).
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np
from scipy import stats


def mann_kendall_test(
    x: Union[List[float], np.ndarray], 
    alpha: float = 0.05,
    modified_for_autocorr: bool = False,
    lag1_autocorr: float = 0.0
) -> Dict[str, Any]:
    """
    Execute the Mann-Kendall non-parametric trend test.
    Handles tied groups and missing values (dropped before calculation).
    """
    series = np.asarray(x, dtype=float)
    valid_mask = ~np.isnan(series)
    clean_x = series[valid_mask]
    n = len(clean_x)

    if n < 4:
        return {
            "n_observations": n,
            "s_statistic": 0.0,
            "var_s": 0.0,
            "z_statistic": 0.0,
            "p_value": 1.0,
            "kendalls_tau": 0.0,
            "trend": "Insufficient Data",
            "is_significant": False,
            "alpha": alpha
        }

    # Calculate Kendall's S
    s = 0.0
    for i in range(n - 1):
        diffs = clean_x[i + 1:] - clean_x[i]
        s += np.sum(np.sign(diffs))

    # Identify ties for variance calculation
    unique_vals, counts = np.unique(clean_x, return_counts=True)
    ties = counts[counts > 1]
    tie_term = np.sum(ties * (ties - 1) * (2 * ties + 5))

    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0

    # Modified Mann-Kendall variance inflation factor for serial autocorrelation
    if modified_for_autocorr and abs(lag1_autocorr) > 0.1:
        # Variance correction factor (Yue & Wang 2004)
        n_eff_factor = 1.0 + 2.0 * (lag1_autocorr / (1.0 - lag1_autocorr)) * (1.0 - (1.0 / n))
        var_s = var_s * max(n_eff_factor, 1.0)

    # Standardized test statistic Z
    std_s = np.sqrt(var_s)
    if s > 0:
        z = (s - 1.0) / std_s
    elif s < 0:
        z = (s + 1.0) / std_s
    else:
        z = 0.0

    # Two-tailed p-value
    p_value = float(2.0 * (1.0 - stats.norm.cdf(abs(z))))

    # Kendall's tau
    total_pairs = n * (n - 1) / 2.0
    tau = s / total_pairs if total_pairs > 0 else 0.0

    # Trend classification
    is_significant = p_value < alpha
    if is_significant:
        trend = "Increasing" if z > 0 else "Decreasing"
    else:
        trend = "No Significant Trend"

    return {
        "n_observations": int(n),
        "s_statistic": float(s),
        "var_s": float(var_s),
        "z_statistic": round(float(z), 4),
        "p_value": round(float(p_value), 5),
        "kendalls_tau": round(float(tau), 4),
        "trend": trend,
        "is_significant": is_significant,
        "alpha": alpha
    }
