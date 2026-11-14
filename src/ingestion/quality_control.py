"""
Quality Control, Validation and Completeness Tracking Module
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Strict scientific protocols:
- Do not treat missing observations as zero.
- Do not silently interpolate missing observations.
- Do not manufacture satellite measurements.
- Track completeness per district and per year.
- Identify invalid values and physical boundary violations.
- Detect and flag duplicate timestamps.
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd


# Physical plausibility limits for Kerala Earth-system variables
PHYSICAL_BOUNDS = {
    "precipitation_mm": {"min": 0.0, "max": 800.0, "unit": "mm/day"},
    "lst_celsius": {"min": 5.0, "max": 52.0, "unit": "°C"},
    "ndvi": {"min": -0.2, "max": 1.0, "unit": "dimensionless"},
    "soil_moisture_m3_m3": {"min": 0.0, "max": 0.65, "unit": "m^3/m^3"},
    "elevation_m": {"min": -10.0, "max": 2800.0, "unit": "meters"},
    "slope_deg": {"min": 0.0, "max": 85.0, "unit": "degrees"}
}


class QualityAssuranceValidator:
    """
    Validates Earth observation time series against physical boundaries,
    quality masks, and structural integrity.
    """

    @staticmethod
    def validate_series(
        values: pd.Series, 
        variable_name: str,
        allow_nan: bool = True
    ) -> Dict[str, Any]:
        """
        Validate a Pandas Series of observations for a named variable.
        Returns detailed QA metrics.
        """
        if variable_name not in PHYSICAL_BOUNDS:
            raise KeyError(f"Unknown variable '{variable_name}'. Known variables: {list(PHYSICAL_BOUNDS.keys())}")

        bounds = PHYSICAL_BOUNDS[variable_name]
        total_count = len(values)
        nan_count = int(values.isna().sum())
        valid_series = values.dropna()
        valid_count = len(valid_series)

        # Physical limit checks
        out_of_bounds_low = int((valid_series < bounds["min"]).sum())
        out_of_bounds_high = int((valid_series > bounds["max"]).sum())
        total_violations = out_of_bounds_low + out_of_bounds_high

        # Completeness calculation
        completeness_pct = (valid_count / total_count * 100.0) if total_count > 0 else 0.0

        is_valid = (total_violations == 0) and (allow_nan or nan_count == 0)

        return {
            "variable": variable_name,
            "total_records": total_count,
            "valid_records": valid_count,
            "missing_records": nan_count,
            "completeness_pct": round(completeness_pct, 2),
            "out_of_bounds_low": out_of_bounds_low,
            "out_of_bounds_high": out_of_bounds_high,
            "physical_min_allowed": bounds["min"],
            "physical_max_allowed": bounds["max"],
            "unit": bounds["unit"],
            "is_valid": is_valid
        }

    @staticmethod
    def check_duplicates(df: pd.DataFrame, time_col: str, district_col: str) -> int:
        """Count duplicate observations for the same district and timestamp."""
        duplicates = df.duplicated(subset=[time_col, district_col]).sum()
        return int(duplicates)


class DataCompletenessReport:
    """
    Computes and aggregates data completeness across all districts, variables,
    and observation years.
    """

    def __init__(self, observation_window: Tuple[int, int] = (2001, 2024)):
        self.start_year, self.end_year = observation_window
        self.total_years = self.end_year - self.start_year + 1

    def assess_completeness_by_year(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        val_col: str, 
        district_col: str = "district",
        expected_per_year: int = 365
    ) -> pd.DataFrame:
        """
        Calculate completeness % for every district and year.
        Ensures missing observations are tracked, never zero-filled.
        """
        temp_df = df.copy()
        temp_df["year"] = pd.to_datetime(temp_df[date_col]).dt.year
        
        # Group by district and year
        grouped = temp_df.groupby([district_col, "year"])[val_col].agg(
            total_observations='count',
            valid_observations=lambda s: int(s.notna().sum()),
            missing_observations=lambda s: int(s.isna().sum())
        ).reset_index()

        grouped["expected_observations"] = expected_per_year
        grouped["completeness_pct"] = (grouped["valid_observations"] / grouped["expected_observations"] * 100.0).clip(upper=100.0).round(2)
        
        return grouped
