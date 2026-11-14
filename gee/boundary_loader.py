"""
MONSOON PULSE — Kerala District Boundary Loader for Google Earth Engine & Python
NASA Space Apps Challenge 2026
"""

import json
from pathlib import Path
from typing import Dict, List, Any


def load_kerala_geojson(path: str = "data/raw/kerala_districts.geojson") -> Dict[str, Any]:
    """Load the official Data{Meet} Kerala district GeoJSON."""
    geo_path = Path(path)
    if not geo_path.exists():
        raise FileNotFoundError(f"District GeoJSON not found at: {geo_path.resolve()}")
    
    with open(geo_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_district_names(geojson_data: Dict[str, Any] = None) -> List[str]:
    """Return sorted list of all 14 Kerala district names."""
    if geojson_data is None:
        geojson_data = load_kerala_geojson()
    names = [f["properties"]["district"] for f in geojson_data["features"]]
    return sorted(list(set(names)))


def to_ee_feature_collection(ee_module, geojson_data: Dict[str, Any] = None):
    """
    Convert GeoJSON to an Earth Engine ee.FeatureCollection.
    Requires ee to be initialized.
    """
    if geojson_data is None:
        geojson_data = load_kerala_geojson()
    
    features = []
    for f in geojson_data["features"]:
        geom = ee_module.Geometry(f["geometry"])
        props = f["properties"]
        features.append(ee_module.Feature(geom, props))
        
    return ee_module.FeatureCollection(features)


if __name__ == "__main__":
    data = load_kerala_geojson()
    districts = get_district_names(data)
    print(f"Loaded {len(districts)} Kerala districts:")
    for d in districts:
        print(f" - {d}")
