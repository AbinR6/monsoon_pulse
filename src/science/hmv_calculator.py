"""
Heat–Moisture–Vegetation (HMV) Compound Indicator Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Project-defined formula:
    HMV = (Z_LST - Z_SMAP - Z_NDVI) / 3

Where:
- Z_LST: Standardized Land-Surface Temperature (MODIS MOD11A2)
- Z_SMAP: Standardized Root-Zone Soil Moisture (NASA SMAP SPL4SMGP)
- Z_NDVI: Standardized Vegetation Index (MODIS MOD13Q1)

Scientific Rationale:
- Concurrent Multi-Sensor Period: 2015–2024 (dictated by NASA SMAP launch).
- Standardization: Z = (X - mu_base) / sigma_base.
- Interpretation:
    Positive HMV (> 0): Concurrent high thermal stress, soil moisture deficit,
    and vegetation degradation.
    Negative HMV (< 0): Cool, moisture-rich, healthy vegetative conditions.
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd


class HmvCalculator:
    """Calculates the project-defined Heat-Moisture-Vegetation (HMV) indicator."""

    def __init__(self, baseline_period: Tuple[int, int] = (2015, 2024)):
        self.baseline_start, self.baseline_end = baseline_period

    def calculate_hmv(
        self,
        df_lst_annual: pd.DataFrame,
        df_smap_annual: pd.DataFrame,
        df_ndvi_annual: pd.DataFrame,
        districts: List[str]
    ) -> pd.DataFrame:
        """
        Merge annual LST, SMAP, and NDVI metrics, calculate Z-scores relative
        to the baseline period, and compute HMV for each district and year.
        """
        results = []

        for dist in districts:
            sub_lst = df_lst_annual[df_lst_annual["district"] == dist].set_index("year")["lst_mean_celsius"]
            sub_smap = df_smap_annual[df_smap_annual["district"] == dist].set_index("year")["sm_mean_m3_m3"]
            sub_ndvi = df_ndvi_annual[df_ndvi_annual["district"] == dist].set_index("year")["ndvi_mean"]

            # Align on common years (2015-2024)
            common_years = sorted(list(set(sub_lst.index).intersection(sub_smap.index).intersection(sub_ndvi.index)))
            if not common_years:
                continue

            merged = pd.DataFrame({
                "lst": sub_lst.loc[common_years],
                "smap": sub_smap.loc[common_years],
                "ndvi": sub_ndvi.loc[common_years]
            }, index=common_years)

            # Compute baseline statistics (mean and std)
            base_mask = (merged.index >= self.baseline_start) & (merged.index <= self.baseline_end)
            base_df = merged.loc[base_mask]

            mu_lst, std_lst = float(base_df["lst"].mean()), float(base_df["lst"].std(ddof=1))
            mu_smap, std_smap = float(base_df["smap"].mean()), float(base_df["smap"].std(ddof=1))
            mu_ndvi, std_ndvi = float(base_df["ndvi"].mean()), float(base_df["ndvi"].std(ddof=1))

            # Protect against zero division
            std_lst = std_lst if std_lst > 1e-6 else 1.0
            std_smap = std_smap if std_smap > 1e-6 else 1.0
            std_ndvi = std_ndvi if std_ndvi > 1e-6 else 1.0

            for yr in common_years:
                raw_lst = float(merged.loc[yr, "lst"])
                raw_smap = float(merged.loc[yr, "smap"])
                raw_ndvi = float(merged.loc[yr, "ndvi"])

                z_lst = (raw_lst - mu_lst) / std_lst
                z_smap = (raw_smap - mu_smap) / std_smap
                z_ndvi = (raw_ndvi - mu_ndvi) / std_ndvi

                hmv = (z_lst - z_smap - z_ndvi) / 3.0

                # Environmental interpretation
                if hmv > 0.5:
                    condition = "High Thermal-Moisture Stress"
                elif hmv < -0.5:
                    condition = "Cool, Moist & Vegetated"
                else:
                    condition = "Equilibrium / Moderate"

                results.append({
                    "district": dist,
                    "year": int(yr),
                    "hmv": round(float(hmv), 3),
                    "z_lst": round(float(z_lst), 3),
                    "z_smap": round(float(z_smap), 3),
                    "z_ndvi": round(float(z_ndvi), 3),
                    "raw_lst_celsius": round(raw_lst, 2),
                    "raw_smap_m3_m3": round(raw_smap, 4),
                    "raw_ndvi": round(raw_ndvi, 4),
                    "condition": condition,
                    "baseline_period": f"{self.baseline_start}–{self.baseline_end}"
                })

        return pd.DataFrame(results)
