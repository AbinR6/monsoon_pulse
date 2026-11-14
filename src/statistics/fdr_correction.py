"""
Benjamini–Hochberg False Discovery Rate (FDR) Multi-Testing Correction Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Controls false discovery rates when simultaneously testing multiple districts
and environmental variables:
- Sort raw p-values: p_(1) <= p_(2) <= ... <= p_(m)
- Compute adjusted q-values:
    q_(i) = min_{j >= i} ( (m / j) * p_(j) )
- Significance classifications:
    - Statistically Significant (FDR-controlled): p < 0.05 AND q < 0.05
    - Marginally Significant (Unadjusted only): p < 0.05 AND q >= 0.05
    - Insignificant: p >= 0.05
    - Insufficient Data
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd


def benjamini_hochberg_correction(
    results: List[Dict[str, Any]], 
    p_value_key: str = "p_value", 
    alpha: float = 0.05
) -> List[Dict[str, Any]]:
    """
    Apply Benjamini-Hochberg False Discovery Rate procedure to a list of test results.
    Appends 'q_value' and 'significance_class' to each dictionary.
    """
    m = len(results)
    if m == 0:
        return []

    # Extract indices and p-values
    p_vals = np.array([float(r.get(p_value_key, 1.0)) for r in results])
    sorted_indices = np.argsort(p_vals)
    sorted_p = p_vals[sorted_indices]

    # Calculate BH adjusted q-values
    # q_(i) = (m / rank) * p_(i), running minimum from end backwards
    ranks = np.arange(1, m + 1)
    raw_q = (m / ranks) * sorted_p
    
    # Cumulative minimum from the right
    adjusted_q = np.minimum.accumulate(raw_q[::-1])[::-1]
    adjusted_q = np.clip(adjusted_q, 0.0, 1.0)

    # Map back to original order
    final_q = np.empty(m)
    final_q[sorted_indices] = adjusted_q

    updated_results = []
    for i, res in enumerate(results):
        item = dict(res)
        raw_p = float(res.get(p_value_key, 1.0))
        q_val = round(float(final_q[i]), 5)
        item["q_value"] = q_val

        # Classification
        if item.get("trend") == "Insufficient Data":
            sig_class = "Insufficient Data"
        elif raw_p < alpha and q_val < alpha:
            sig_class = "Statistically Significant (FDR-Controlled)"
        elif raw_p < alpha and q_val >= alpha:
            sig_class = "Marginally Significant (Unadjusted Only)"
        else:
            sig_class = "Statistically Insignificant"

        item["significance_class"] = sig_class
        updated_results.append(item)

    return updated_results
