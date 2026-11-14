"""
Scientific Units Conversion and Physical Scaling Module
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Handles strict physical unit conversions for:
1. MODIS LST: Raw Digital Number (DN) * 0.02 = Kelvin -> Celsius
2. MODIS NDVI: Raw DN * 0.0001 -> Dimensionless [-0.2, 1.0]
3. GPM IMERG: Half-hourly rate (mm/hr) * 0.5 hr -> Daily rainfall (mm)
4. SMAP Root-zone Soil Moisture: Volumetric fraction (m^3/m^3)
5. SRTM: Elevation (m) and Slope (degrees)
"""

import numpy as np
from typing import Union


def kelvin_to_celsius(kelvin: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert temperature from Kelvin to Celsius.
    Formula: T_C = T_K - 273.15
    """
    return kelvin - 273.15


def scale_modis_lst(raw_dn: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Scale MODIS MOD11A2 raw DN to Celsius.
    MODIS LST scale factor is 0.02 (output in Kelvin).
    Then converted to Celsius.
    """
    kelvin = raw_dn * 0.02
    return kelvin_to_celsius(kelvin)


def scale_ndvi(raw_dn: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Scale MODIS MOD13Q1 raw DN to dimensionless NDVI.
    Scale factor is 0.0001. Valid range: -0.2 to 1.0.
    """
    return raw_dn * 0.0001


def mm_per_hr_to_daily_sum(rates_mm_per_hr: np.ndarray, interval_hours: float = 0.5) -> float:
    """
    Integrate precipitation rates (mm/hr) across half-hourly observation intervals
    to calculate daily accumulated rainfall in mm.
    """
    return float(np.sum(rates_mm_per_hr * interval_hours))


def normalize_slope(slope_deg: Union[float, np.ndarray], 
                    min_slope: float, 
                    max_slope: float) -> Union[float, np.ndarray]:
    """
    Min-Max normalize terrain slope to [0, 1] relative to regional bounds.
    Formula: S_norm = (S - S_min) / (S_max - S_min)
    """
    if max_slope == min_slope:
        return 0.0
    return (slope_deg - min_slope) / (max_slope - min_slope)
