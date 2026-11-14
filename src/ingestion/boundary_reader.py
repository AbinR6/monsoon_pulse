"""
District Boundary Ingestion Module for Kerala
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_districts(filepath: Optional[str] = None) -> Dict[str, Any]:
    """
    Load Kerala district boundaries from GeoJSON.
    Defaults to data/raw/kerala_districts.geojson.
    """
    if filepath is None:
        filepath = Path(__file__).resolve().parent.parent.parent / "data" / "raw" / "kerala_districts.geojson"
    else:
        filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Kerala district GeoJSON not found at: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "features" not in data or len(data["features"]) != 14:
        raise ValueError(f"Expected 14 district features in GeoJSON, found {len(data.get('features', []))}")

    return data


def get_district_list(filepath: Optional[str] = None) -> List[str]:
    """Return sorted list of the 14 official district names in Kerala."""
    geojson = load_districts(filepath)
    districts = [f["properties"]["district"] for f in geojson["features"]]
    return sorted(list(set(districts)))


def get_district_metadata() -> Dict[str, Dict[str, Any]]:
    """
    Return geographical and physiographic metadata for Kerala's 14 districts.
    Includes physiographic zone (Coastal/Midland/Highland), headquarters, and area.
    """
    return {
        "Alappuzha": {
            "zone": "Coastal / Lowland",
            "headquarters": "Alappuzha",
            "area_sq_km": 1414,
            "characteristics": "Kuttanad wetland system, deltaic coastal plain, parts below sea level",
            "mean_elevation_m": 4.5,
            "mean_slope_deg": 0.82
        },
        "Ernakulam": {
            "zone": "Coastal / Midland",
            "headquarters": "Kochi",
            "area_sq_km": 3068,
            "characteristics": "Commercial center, Cochin backwaters, Periyar and Muvattupuzha river basins",
            "mean_elevation_m": 22.0,
            "mean_slope_deg": 3.15
        },
        "Idukki": {
            "zone": "Highland / Western Ghats",
            "headquarters": "Painavu",
            "area_sq_km": 4358,
            "characteristics": "High mountain terrain, Anamudi peak (2695m), major hydroelectric reservoirs",
            "mean_elevation_m": 940.0,
            "mean_slope_deg": 18.65
        },
        "Kannur": {
            "zone": "Coastal / Midland / Highland",
            "headquarters": "Kannur",
            "area_sq_km": 2966,
            "characteristics": "Northern coastal stretch with rugged Ghats escarpments",
            "mean_elevation_m": 145.0,
            "mean_slope_deg": 7.85
        },
        "Kasaragod": {
            "zone": "Coastal / Midland",
            "headquarters": "Kasaragod",
            "area_sq_km": 1992,
            "characteristics": "Northernmost district, laterite plateaus and river systems",
            "mean_elevation_m": 115.0,
            "mean_slope_deg": 5.90
        },
        "Kollam": {
            "zone": "Coastal / Midland / Highland",
            "headquarters": "Kollam",
            "area_sq_km": 2491,
            "characteristics": "Ashtamudi Lake estuary, mineral sand coast, Shendurney wildlife sanctuary",
            "mean_elevation_m": 120.0,
            "mean_slope_deg": 6.10
        },
        "Kottayam": {
            "zone": "Midland / Highland",
            "headquarters": "Kottayam",
            "area_sq_km": 2208,
            "characteristics": "Rubber plantations, Vembanad eastern shores, Meenachil river basin",
            "mean_elevation_m": 135.0,
            "mean_slope_deg": 6.45
        },
        "Kozhikode": {
            "zone": "Coastal / Midland / Highland",
            "headquarters": "Kozhikode",
            "area_sq_km": 2344,
            "characteristics": "Malabar coast, Chaliyar river basin, Western Ghats western slopes",
            "mean_elevation_m": 130.0,
            "mean_slope_deg": 8.45
        },
        "Malappuram": {
            "zone": "Coastal / Midland / Highland",
            "headquarters": "Malappuram",
            "area_sq_km": 3550,
            "characteristics": "Rolling lateritic hills, Bharathapuzha and Chaliyar river basins, Nilambur forests",
            "mean_elevation_m": 140.0,
            "mean_slope_deg": 8.10
        },
        "Palakkad": {
            "zone": "Inland Valley / Gap",
            "headquarters": "Palakkad",
            "area_sq_km": 4480,
            "characteristics": "Palakkad Gap (30km mountain pass), thermal hotspot, granary of Kerala",
            "mean_elevation_m": 165.0,
            "mean_slope_deg": 9.20
        },
        "Pathanamthitta": {
            "zone": "Midland / Highland",
            "headquarters": "Pathanamthitta",
            "area_sq_km": 2637,
            "characteristics": "Heavily forested Ghats, Pamba and Achenkovil river systems",
            "mean_elevation_m": 310.0,
            "mean_slope_deg": 13.80
        },
        "Thiruvananthapuram": {
            "zone": "Coastal / Midland / Highland",
            "headquarters": "Thiruvananthapuram",
            "area_sq_km": 2189,
            "characteristics": "State capital, southern tip, Agasthyamalai biosphere, dual monsoon exposure",
            "mean_elevation_m": 125.0,
            "mean_slope_deg": 7.50
        },
        "Thrissur": {
            "zone": "Coastal / Midland / Highland",
            "headquarters": "Thrissur",
            "area_sq_km": 3032,
            "characteristics": "Kole wetlands, central cultural capital, Chalakudy and Karuvannur rivers",
            "mean_elevation_m": 95.0,
            "mean_slope_deg": 7.15
        },
        "Wayanad": {
            "zone": "Highland / Western Ghats",
            "headquarters": "Kalpetta",
            "area_sq_km": 2131,
            "characteristics": "Elevated Nilgiri biosphere plateau (700-2100m), steep landslide-prone escarpments",
            "mean_elevation_m": 880.0,
            "mean_slope_deg": 15.35
        }
    }
