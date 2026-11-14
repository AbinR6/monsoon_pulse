"""
ETCCDI R95p Extreme Precipitation Calculator
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Methodology conforms to the Expert Team on Climate Change Detection and Indices (ETCCDI):
- Wet day definition: Daily precipitation P_d >= 1.0 mm.
- Reference baseline period: Defined base years (default: 2001–2020).
- 95th Percentile (P95): Computed from all wet days within the baseline period.
- Annual R95p: Total precipitation on wet days exceeding the reference P95:
    R95p = sum(P_d for d in wet_days where P_d > P95) [mm]
- Seasonal JJAS R95p: Same extreme threshold applied to June–September monsoon days.
- Distinguishes annual R95p from seasonal JJAS R95p.
- Completeness requirements: Flag years with <85% valid daily records.
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd


class R95pCalculator:
    """Calculates ETCCDI R95p extreme precipitation metrics."""

    def __init__(
        self, 
        wet_day_threshold_mm: float = 1.0, 
        baseline_period: Tuple[int, int] = (2001, 2020),
        min_completeness_pct: float = 85.0
    ):
        self.wet_day_threshold = wet_day_threshold_mm
        self.baseline_start, self.baseline_end = baseline_period
        self.min_completeness_pct = min_completeness_pct

    def compute_district_threshold(self, df_district: pd.DataFrame) -> float:
        """
        Compute the 95th percentile of daily precipitation on wet days (P >= 1.0 mm)
        during the baseline reference period (e.g. 2001–2020).
        """
        # Filter to baseline period and wet days
        base_mask = (df_district["year"] >= self.baseline_start) & (df_district["year"] <= self.baseline_end)
        wet_mask = df_district["precipitation_mm"] >= self.wet_day_threshold
        valid_mask = df_district["precipitation_mm"].notna()
        
        baseline_wet_days = df_district.loc[base_mask & wet_mask & valid_mask, "precipitation_mm"]
        if len(baseline_wet_days) < 30:
            raise ValueError(f"Insufficient baseline wet days ({len(baseline_wet_days)}) to compute 95th percentile.")
        
        p95 = float(np.percentile(baseline_wet_days, 95))
        return round(p95, 2)

    def calculate_annual_r95p(
        self, 
        df_district: pd.DataFrame, 
        threshold_p95: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Calculate annual and seasonal JJAS R95p time series for a district.
        """
        if threshold_p95 is None:
            threshold_p95 = self.compute_district_threshold(df_district)

        results = []
        years = sorted(df_district["year"].unique())

        for yr in years:
            yr_df = df_district[df_district["year"] == yr]
            total_days = len(yr_df)
            valid_days = int(yr_df["precipitation_mm"].notna().sum())
            completeness = (valid_days / 365.0 * 100.0) if total_days > 0 else 0.0
            is_complete = completeness >= self.min_completeness_pct

            # Wet days
            wet_days = yr_df[yr_df["precipitation_mm"] >= self.wet_day_threshold]
            prcptot = float(wet_days["precipitation_mm"].sum())
            wet_day_count = len(wet_days)

            # Annual R95p
            extreme_days = wet_days[wet_days["precipitation_mm"] > threshold_p95]
            r95p_annual = float(extreme_days["precipitation_mm"].sum())
            extreme_day_count = len(extreme_days)
            r95p_fraction = (r95p_annual / prcptot * 100.0) if prcptot > 0 else 0.0

            # Max 1-day rainfall (RX1day)
            rx1day = float(yr_df["precipitation_mm"].max()) if valid_days > 0 else np.nan

            # JJAS Monsoon (June-September)
            jjas_df = yr_df[yr_df["month"].isin([6, 7, 8, 9])]
            jjas_wet = jjas_df[jjas_df["precipitation_mm"] >= self.wet_day_threshold]
            jjas_prcptot = float(jjas_wet["precipitation_mm"].sum())
            jjas_extreme = jjas_wet[jjas_wet["precipitation_mm"] > threshold_p95]
            r95p_jjas = float(jjas_extreme["precipitation_mm"].sum())
            jjas_extreme_count = len(jjas_extreme)

            district_name = yr_df["district"].iloc[0]

            results.append({
                "district": district_name,
                "year": int(yr),
                "threshold_p95_mm": threshold_p95,
                "r95p_annual_mm": round(r95p_annual, 2),
                "r95p_jjas_mm": round(r95p_jjas, 2),
                "r95p_fraction_pct": round(r95p_fraction, 2),
                "prcptot_annual_mm": round(prcptot, 2),
                "prcptot_jjas_mm": round(jjas_prcptot, 2),
                "extreme_days_count": extreme_day_count,
                "jjas_extreme_days_count": jjas_extreme_count,
                "wet_days_count": wet_day_count,
                "rx1day_mm": round(rx1day, 2),
                "completeness_pct": round(min(completeness, 100.0), 2),
                "is_complete": is_complete
            })

        return pd.DataFrame(results)
