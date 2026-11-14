"""
Sensitivity Analysis Engine for Methodological Assumptions
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Evaluates stability of scientific conclusions across alternative methodological choices:
1. R95p Baseline Window: Standard 2001–2020 vs Full 2001–2024
2. Wet-Day Threshold: Standard 1.0 mm/day vs 2.5 mm/day (heavy wet day)
3. HMV Baseline Window: 2015–2020 vs 2015–2024
4. RTE Terrain Slope Metric: Mean Slope vs 90th Percentile Slope
"""

from typing import Dict, List, Any
import numpy as np
import pandas as pd

from src.science.r95p_calculator import R95pCalculator
from src.science.hmv_calculator import HmvCalculator
from src.science.rte_calculator import RteCalculator
from src.statistics.mann_kendall import mann_kendall_test
from src.statistics.theil_sen import theil_sen_estimator


class SensitivityTester:
    """Executes multi-scenario sensitivity analyses."""

    @staticmethod
    def test_r95p_baseline_sensitivity(df_precip: pd.DataFrame, district: str) -> Dict[str, Any]:
        """Compare R95p metrics under 2001–2020 baseline vs 2001–2024 baseline."""
        sub = df_precip[df_precip["district"] == district]
        
        calc_std = R95pCalculator(baseline_period=(2001, 2020))
        calc_full = R95pCalculator(baseline_period=(2001, 2024))

        p95_std = calc_std.compute_district_threshold(sub)
        p95_full = calc_full.compute_district_threshold(sub)

        ts_std = calc_std.calculate_annual_r95p(sub, threshold_p95=p95_std)
        ts_full = calc_full.calculate_annual_r95p(sub, threshold_p95=p95_full)

        mean_r95p_std = float(ts_std["r95p_annual_mm"].mean())
        mean_r95p_full = float(ts_full["r95p_annual_mm"].mean())
        pct_diff = ((mean_r95p_full - mean_r95p_std) / mean_r95p_std * 100.0) if mean_r95p_std > 0 else 0.0

        # Trend comparison
        mk_std = mann_kendall_test(ts_std["r95p_annual_mm"].values)
        mk_full = mann_kendall_test(ts_full["r95p_annual_mm"].values)

        return {
            "district": district,
            "parameter": "R95p Baseline Period",
            "scenario_a": {"name": "Standard Reference (2001–2020)", "threshold_p95_mm": p95_std, "mean_annual_r95p_mm": round(mean_r95p_std, 2), "p_value": mk_std["p_value"]},
            "scenario_b": {"name": "Full Period Reference (2001–2024)", "threshold_p95_mm": p95_full, "mean_annual_r95p_mm": round(mean_r95p_full, 2), "p_value": mk_full["p_value"]},
            "pct_difference": round(pct_diff, 2),
            "trend_concordance": mk_std["trend"] == mk_full["trend"],
            "conclusion": "Trend direction robust across baseline periods" if mk_std["trend"] == mk_full["trend"] else "Sensitive to baseline period"
        }

    @staticmethod
    def test_wet_day_threshold_sensitivity(df_precip: pd.DataFrame, district: str) -> Dict[str, Any]:
        """Compare R95p under 1.0 mm wet-day threshold vs 2.5 mm wet-day threshold."""
        sub = df_precip[df_precip["district"] == district]
        
        calc_1mm = R95pCalculator(wet_day_threshold_mm=1.0)
        calc_2_5mm = R95pCalculator(wet_day_threshold_mm=2.5)

        p95_1mm = calc_1mm.compute_district_threshold(sub)
        p95_2_5mm = calc_2_5mm.compute_district_threshold(sub)

        ts_1mm = calc_1mm.calculate_annual_r95p(sub, threshold_p95=p95_1mm)
        ts_2_5mm = calc_2_5mm.calculate_annual_r95p(sub, threshold_p95=p95_2_5mm)

        mk_1mm = mann_kendall_test(ts_1mm["r95p_annual_mm"].values)
        mk_2_5mm = mann_kendall_test(ts_2_5mm["r95p_annual_mm"].values)

        return {
            "district": district,
            "parameter": "Wet-Day Threshold",
            "scenario_a": {"name": "Standard 1.0 mm/day", "threshold_p95_mm": p95_1mm, "p_value": mk_1mm["p_value"]},
            "scenario_b": {"name": "Heavy 2.5 mm/day", "threshold_p95_mm": p95_2_5mm, "p_value": mk_2_5mm["p_value"]},
            "trend_concordance": mk_1mm["trend"] == mk_2_5mm["trend"],
            "conclusion": "Methodologically consistent" if mk_1mm["trend"] == mk_2_5mm["trend"] else "Moderate threshold sensitivity"
        }
