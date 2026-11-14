"""
Autocorrelation and Serial Dependency Assessment
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Computes:
- Lag-1 serial autocorrelation coefficient (r1).
- Anderson 95% confidence limits for independent series:
    CI = (-1 +- 1.96 * sqrt(n - 2)) / (n - 1)
- Identifies whether serial autocorrelation is statistically significant.
- Determines if Modified Mann-Kendall variance correction is warranted.
"""

from typing import Dict, List, Any, Union
import numpy as np


def assess_autocorrelation(x: Union[List[float], np.ndarray], alpha: float = 0.05) -> Dict[str, Any]:
    """
    Compute lag-1 autocorrelation coefficient and test for statistical significance.
    """
    arr = np.asarray(x, dtype=float)
    clean = arr[~np.isnan(arr)]
    n = len(clean)

    if n < 5:
        return {
            "n_observations": n,
            "lag1_autocorr": 0.0,
            "anderson_lower": -1.0,
            "anderson_upper": 1.0,
            "is_significant": False,
            "recommendation": "Standard Mann-Kendall"
        }

    mean_val = np.mean(clean)
    diff = clean - mean_val
    denominator = np.sum(diff ** 2)

    if denominator < 1e-9:
        return {
            "n_observations": n,
            "lag1_autocorr": 0.0,
            "anderson_lower": -1.0,
            "anderson_upper": 1.0,
            "is_significant": False,
            "recommendation": "Standard Mann-Kendall"
        }

    numerator = np.sum(diff[:-1] * diff[1:])
    r1 = numerator / denominator

    # Anderson 95% two-tailed test bounds for white noise
    z_crit = 1.96
    lower_bound = (-1.0 - z_crit * np.sqrt(n - 2)) / (n - 1)
    upper_bound = (-1.0 + z_crit * np.sqrt(n - 2)) / (n - 1)

    is_significant = (r1 < lower_bound) or (r1 > upper_bound)
    recommendation = "Modified Mann-Kendall (Yue & Wang)" if is_significant else "Standard Mann-Kendall"

    return {
        "n_observations": int(n),
        "lag1_autocorr": round(float(r1), 4),
        "anderson_lower": round(float(lower_bound), 4),
        "anderson_upper": round(float(upper_bound), 4),
        "is_significant": bool(is_significant),
        "recommendation": recommendation
    }
