"""
Temporal Aggregation and Seasonal Climatology Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Strict rules:
- Do not treat missing observations as zero.
- Do not silently interpolate missing observations.
- Minimum data completeness requirement: 80% for annual aggregation.
- Seasons:
    - South-West Monsoon (JJAS: Jun, Jul, Aug, Sep)
    - North-East Monsoon (OND: Oct, Nov, Dec)
    - Pre-monsoon Summer (MAM: Mar, Apr, May)
    - Winter (JF: Jan, Feb)
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


class TemporalAggregator:
    """Aggregates sub-annual satellite series to annual and seasonal levels."""

    @staticmethod
    def aggregate_lst_annual(df_lst: pd.DataFrame, min_completeness_pct: float = 75.0) -> pd.DataFrame:
        """
        Aggregate 8-day MODIS LST to annual metrics per district.
        Expected observations per year: ~46 composites.
        """
        results = []
        for (dist, yr), grp in df_lst.groupby(["district", "year"]):
            valid_s = grp["lst_celsius"].dropna()
            total_obs = len(grp)
            valid_obs = len(valid_s)
            completeness = (valid_obs / 46.0 * 100.0)

            if valid_obs >= 25: # minimum valid composites
                mean_lst = float(valid_s.mean())
                median_lst = float(valid_s.median())
                max_lst = float(valid_s.max())
                min_lst = float(valid_s.min())
                std_lst = float(valid_s.std(ddof=1)) if valid_obs > 1 else 0.0
            else:
                mean_lst = np.nan
                median_lst = np.nan
                max_lst = np.nan
                min_lst = np.nan
                std_lst = np.nan

            results.append({
                "district": dist,
                "year": int(yr),
                "lst_mean_celsius": round(mean_lst, 2) if not np.isnan(mean_lst) else np.nan,
                "lst_median_celsius": round(median_lst, 2) if not np.isnan(median_lst) else np.nan,
                "lst_max_celsius": round(max_lst, 2) if not np.isnan(max_lst) else np.nan,
                "lst_min_celsius": round(min_lst, 2) if not np.isnan(min_lst) else np.nan,
                "lst_std_celsius": round(std_lst, 2) if not np.isnan(std_lst) else np.nan,
                "valid_observations": valid_obs,
                "total_observations": total_obs,
                "completeness_pct": round(min(completeness, 100.0), 2),
                "is_complete": completeness >= min_completeness_pct
            })

        return pd.DataFrame(results)

    @staticmethod
    def aggregate_ndvi_annual(df_ndvi: pd.DataFrame, min_completeness_pct: float = 75.0) -> pd.DataFrame:
        """
        Aggregate 16-day MODIS NDVI to annual metrics per district.
        Expected observations per year: ~23 composites.
        """
        results = []
        for (dist, yr), grp in df_ndvi.groupby(["district", "year"]):
            valid_s = grp["ndvi"].dropna()
            total_obs = len(grp)
            valid_obs = len(valid_s)
            completeness = (valid_obs / 23.0 * 100.0)

            if valid_obs >= 14:
                mean_ndvi = float(valid_s.mean())
                median_ndvi = float(valid_s.median())
                max_ndvi = float(valid_s.max())
                min_ndvi = float(valid_s.min())
            else:
                mean_ndvi = np.nan
                median_ndvi = np.nan
                max_ndvi = np.nan
                min_ndvi = np.nan

            results.append({
                "district": dist,
                "year": int(yr),
                "ndvi_mean": round(mean_ndvi, 4) if not np.isnan(mean_ndvi) else np.nan,
                "ndvi_median": round(median_ndvi, 4) if not np.isnan(median_ndvi) else np.nan,
                "ndvi_max": round(max_ndvi, 4) if not np.isnan(max_ndvi) else np.nan,
                "ndvi_min": round(min_ndvi, 4) if not np.isnan(min_ndvi) else np.nan,
                "valid_observations": valid_obs,
                "total_observations": total_obs,
                "completeness_pct": round(min(completeness, 100.0), 2),
                "is_complete": completeness >= min_completeness_pct
            })

        return pd.DataFrame(results)

    @staticmethod
    def aggregate_smap_annual(df_smap: pd.DataFrame, min_completeness_pct: float = 85.0) -> pd.DataFrame:
        """
        Aggregate daily SMAP root-zone soil moisture to annual metrics per district.
        Expected observations per year: 365 days.
        """
        results = []
        for (dist, yr), grp in df_smap.groupby(["district", "year"]):
            valid_s = grp["soil_moisture_m3_m3"].dropna()
            total_obs = len(grp)
            valid_obs = len(valid_s)
            completeness = (valid_obs / 365.0 * 100.0)

            if valid_obs >= 250:
                mean_sm = float(valid_s.mean())
                median_sm = float(valid_s.median())
                max_sm = float(valid_s.max())
                min_sm = float(valid_s.min())
            else:
                mean_sm = np.nan
                median_sm = np.nan
                max_sm = np.nan
                min_sm = np.nan

            results.append({
                "district": dist,
                "year": int(yr),
                "sm_mean_m3_m3": round(mean_sm, 4) if not np.isnan(mean_sm) else np.nan,
                "sm_median_m3_m3": round(median_sm, 4) if not np.isnan(median_sm) else np.nan,
                "sm_max_m3_m3": round(max_sm, 4) if not np.isnan(max_sm) else np.nan,
                "sm_min_m3_m3": round(min_sm, 4) if not np.isnan(min_sm) else np.nan,
                "valid_observations": valid_obs,
                "total_observations": total_obs,
                "completeness_pct": round(min(completeness, 100.0), 2),
                "is_complete": completeness >= min_completeness_pct
            })

        return pd.DataFrame(results)
