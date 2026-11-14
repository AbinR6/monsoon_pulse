"""
Satellite Dataset Loader and Harmonization Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Loads, cleans, validates, and harmonizes:
1. NASA GPM IMERG V07 Precipitation (2001–2024)
2. MODIS MOD11A2 V6.1 Land Surface Temperature (2001–2024)
3. MODIS MOD13Q1 V6.1 Vegetation Indices (NDVI) (2001–2024)
4. NASA SMAP SPL4SMGP V008 Root-Zone Soil Moisture (2015–2024)
5. NASA/USGS SRTMGL1 V003 Elevation & Terrain Slope
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

from src.ingestion.quality_control import QualityAssuranceValidator
from src.ingestion.units_converter import kelvin_to_celsius, scale_ndvi


class DatasetLoader:
    """Central loader for all MONSOON PULSE Earth-observation datasets."""

    def __init__(self, raw_data_dir: Optional[str] = None):
        if raw_data_dir is None:
            self.raw_dir = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
        else:
            self.raw_dir = Path(raw_data_dir)

    def load_precipitation(self) -> pd.DataFrame:
        """
        Load GPM IMERG daily precipitation (2001–2024).
        Columns: [date, district, precipitation_mm, quality_flag]
        """
        csv_path = self.raw_dir / "gpm_imerg_daily_2001_2024.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"GPM IMERG data not found at {csv_path}")

        df = pd.read_csv(csv_path)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        return df

    def load_lst(self) -> pd.DataFrame:
        """
        Load MODIS MOD11A2 Land Surface Temperature (2001–2024).
        Columns: [date, district, lst_celsius, qc_flag]
        """
        csv_path = self.raw_dir / "modis_lst_8day_2001_2024.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"MODIS LST data not found at {csv_path}")

        df = pd.read_csv(csv_path)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        return df

    def load_ndvi(self) -> pd.DataFrame:
        """
        Load MODIS MOD13Q1 Vegetation Indices (2001–2024).
        Columns: [date, district, ndvi, summary_qa]
        """
        csv_path = self.raw_dir / "modis_ndvi_16day_2001_2024.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"MODIS NDVI data not found at {csv_path}")

        df = pd.read_csv(csv_path)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        return df

    def load_soil_moisture(self) -> pd.DataFrame:
        """
        Load NASA SMAP Root-Zone Soil Moisture (2015–2024).
        Columns: [date, district, soil_moisture_m3_m3, quality_flag]
        Note: Shorter temporal window (2015-2024).
        """
        csv_path = self.raw_dir / "smap_soil_moisture_2015_2024.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"SMAP soil moisture data not found at {csv_path}")

        df = pd.read_csv(csv_path)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        return df

    def load_terrain(self) -> Dict[str, Any]:
        """
        Load NASA/USGS SRTM terrain statistics per district.
        Returns dictionary keyed by district name.
        """
        json_path = self.raw_dir / "srtm_terrain_statistics.json"
        if not json_path.exists():
            raise FileNotFoundError(f"SRTM terrain statistics not found at {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
