"""
Rainfall–Terrain Exposure (RTE) Screening Indicator Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Project-defined formula:
    RTE = Z_R95p,JJAS * S_norm

Where:
- Z_R95p,JJAS: Standardized June–September (JJAS) extreme precipitation (R95p)
- S_norm: Min-Max normalized district mean terrain slope derived from SRTMGL1 V003:
    S_norm = (S_d - S_min) / (S_max - S_min)

Scientific & Screening Rationale:
- Identifies geographical regions where extreme monsoon rainfall coincides with
  high topographical slope exposure.
- Distinct from landslide occurrence: RTE is a screening indicator of combined
  hydro-meteorological and topographical exposure.
- Displays rainfall and terrain contributions separately.
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd


class RteCalculator:
    """Calculates the Rainfall-Terrain Exposure (RTE) index."""

    def __init__(self, terrain_stats: Dict[str, Any]):
        self.terrain_stats = terrain_stats

    def calculate_rte(self, df_r95p: pd.DataFrame) -> pd.DataFrame:
        """
        Compute RTE for all districts and years (2001–2024).
        Calculates standardized JJAS R95p (Z_R95p,JJAS) per district and multiplies by S_norm.
        """
        results = []
        districts = sorted(df_r95p["district"].unique())

        for dist in districts:
            if dist not in self.terrain_stats:
                continue

            sub_df = df_r95p[df_r95p["district"] == dist].copy()
            norm_slope = float(self.terrain_stats[dist]["normalized_slope"])
            mean_slope = float(self.terrain_stats[dist]["mean_slope_deg"])
            elev_mean = float(self.terrain_stats[dist]["mean_elevation_m"])
            p90_slope = float(self.terrain_stats[dist]["p90_slope_deg"])

            # Compute district JJAS R95p mean and std over the historical period
            vals = sub_df["r95p_jjas_mm"].values
            mu_r95p = float(np.nanmean(vals))
            std_r95p = float(np.nanstd(vals, ddof=1))
            std_r95p = std_r95p if std_r95p > 1e-4 else 1.0

            for _, row in sub_df.iterrows():
                yr = int(row["year"])
                raw_r95p_jjas = float(row["r95p_jjas_mm"])

                z_r95p = (raw_r95p_jjas - mu_r95p) / std_r95p
                rte = z_r95p * norm_slope

                # Exposure categorization
                if rte > 1.0:
                    exposure_level = "Very High Exposure"
                elif rte > 0.4:
                    exposure_level = "High Exposure"
                elif rte > -0.2:
                    exposure_level = "Moderate Exposure"
                else:
                    exposure_level = "Low Exposure"

                results.append({
                    "district": dist,
                    "year": yr,
                    "rte": round(float(rte), 3),
                    "z_r95p_jjas": round(float(z_r95p), 3),
                    "normalized_slope": round(norm_slope, 4),
                    "mean_slope_deg": mean_slope,
                    "p90_slope_deg": p90_slope,
                    "mean_elevation_m": elev_mean,
                    "raw_r95p_jjas_mm": round(raw_r95p_jjas, 2),
                    "exposure_level": exposure_level,
                    "rainfall_contribution": round(float(z_r95p), 3),
                    "terrain_contribution": round(norm_slope, 4)
                })

        return pd.DataFrame(results)
