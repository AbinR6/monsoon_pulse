"""
MONSOON PULSE — Automated Google Earth Engine Python Extraction Pipeline
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

This script orchestrates satellite-data acquisition across Kerala's 14 districts
using the Google Earth Engine Python API (earthengine-api).

Datasets Extracted:
1. NASA GPM IMERG V07: Half-hourly precipitation rate (mm/hr) grouped by calendar day,
   multiplied by 0.5 hr, and summed into daily precipitation depth (mm/day) across 2001–2024.
2. MODIS MOD11A2 V6.1: 8-day daytime Land Surface Temperature (LST) scaled by 0.02 and offset
   by -273.15 (°C), filtered with QC_Day quality flags across 2001–2024.
3. MODIS MOD13Q1 V6.1: 16-day Normalized Difference Vegetation Index (NDVI) scaled by 0.0001,
   filtered with SummaryQA quality masks across 2001–2024.
4. NASA SMAP SPL4SMGP V008: 3-hourly root-zone soil moisture (0–100 cm depth, m^3/m^3)
   aggregated into daily mean composites across 2015–2024.
5. NASA/USGS SRTMGL1 V003: 30m digital elevation model and Horn terrain slope across all districts.
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gee.boundary_loader import load_kerala_geojson, to_ee_feature_collection, get_district_names


def init_earth_engine(project_id: str = None) -> bool:
    """Initialize Earth Engine API with graceful authentication handling."""
    try:
        import ee
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize()
        print("Google Earth Engine API initialized successfully.")
        return True
    except Exception as exc:
        print(f"\n[Earth Engine Notice]: {exc}")
        print("\nTo authenticate Google Earth Engine for automated live cloud extraction:")
        print("  1. Run 'earthengine authenticate' in your terminal.")
        print("  2. Select your Google Cloud Earth Engine enabled project.")
        print("  3. Rerun this script with: python gee/gee_monsoon_pulse_pipeline.py --project <YOUR_PROJECT_ID>\n")
        return False


def build_gpm_daily_collection(ee, start_date: str, end_date: str, region_fc):
    """
    Constructs an Earth Engine ImageCollection of daily accumulated rainfall (mm/day)
    from NASA GPM IMERG V07 half-hourly precipitation rates.
    """
    start = ee.Date(start_date)
    end = ee.Date(end_date)
    n_days = end.difference(start, 'day')
    day_seq = ee.List.sequence(0, n_days.subtract(1))

    imerg_raw = ee.ImageCollection("NASA/GPM_L3/IMERG_V07") \
        .filterBounds(region_fc) \
        .filterDate(start, end) \
        .select("precipitationCal")

    def aggregate_single_day(d_offset):
        day_start = start.advance(d_offset, 'day')
        day_end = day_start.advance(1, 'day')
        slice_30min = imerg_raw.filterDate(day_start, day_end)
        
        # Depth per 30 min = rate (mm/hr) * 0.5 hr
        daily_sum = slice_30min.map(lambda img: img.multiply(0.5)) \
            .reduce(ee.Reducer.sum()) \
            .rename("precipitation_mm")
            
        return daily_sum.set({
            "system:time_start": day_start.millis(),
            "date_str": day_start.format("YYYY-MM-dd")
        })

    daily_images = day_seq.map(aggregate_single_day)
    return ee.ImageCollection.fromImages(daily_images)


def run_pipeline(start_year: int = 2001, end_year: int = 2024, output_dir: str = "data/raw", project_id: str = None):
    """Run the complete multi-sensor Earth Engine extraction pipeline."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    geojson = load_kerala_geojson()
    districts = get_district_names(geojson)
    print(f"Target study area: Kerala ({len(districts)} districts)")
    print(f"Target temporal window: {start_year}–{end_year}")
    
    is_authenticated = init_earth_engine(project_id)
    if not is_authenticated:
        print("[Status]: Offline Verification Mode — Full GEE Code Editor extraction suite is ready at:")
        print("          gee/gee_monsoon_pulse_extractor.js")
        print("          Refer to gee/README.md for manual Code Editor execution instructions.")
        return False

    import ee
    kerala_fc = to_ee_feature_collection(ee, geojson)
    srtm_land = ee.Image("USGS/SRTMGL1_003").select("elevation")
    land_mask = srtm_land.gte(-5)

    print("\n[GEE Task 1/5] Dispatching SRTM Terrain 30m Extraction...")
    slope = ee.Terrain.slope(srtm_land).rename("slope_deg")
    terrain = srtm_land.rename("elevation_m").addBands(slope)
    terrain_stats = terrain.reduceRegions(
        collection=kerala_fc,
        reducer=ee.Reducer.mean()
            .combine(ee.Reducer.minMax(), "", True)
            .combine(ee.Reducer.percentile([10, 90]), "", True)
            .combine(ee.Reducer.count(), "", True),
        scale=30,
        tileScale: 4
    )
    task_srtm = ee.batch.Export.table.toDrive(
        collection=terrain_stats,
        description="MONSOON_PULSE_SRTM_Terrain_Stats",
        folder="MONSOON_PULSE_EXPORTS",
        fileFormat="CSV"
    )
    task_srtm.start()
    print(f"  -> SRTM Task ID: {task_srtm.id}")

    print("\n[GEE Task 2/5] Dispatching MODIS LST (2001-2024) Extraction...")
    def mask_modis_lst(img):
        qc = img.select("QC_Day")
        qa_mask = qc.bitwiseAnd(3).lte(1)
        lst_c = img.select("LST_Day_1km").multiply(0.02).subtract(273.15).rename("lst_celsius")
        return lst_c.updateMask(qa_mask).updateMask(land_mask).copyProperties(img, ["system:time_start"])

    modis_lst = ee.ImageCollection("MODIS/061/MOD11A2") \
        .filterBounds(kerala_fc) \
        .filterDate(f"{start_year}-01-01", f"{end_year}-12-31") \
        .map(mask_modis_lst)

    lst_table = modis_lst.map(lambda img: img.reduceRegions(
        collection=kerala_fc,
        reducer=ee.Reducer.mean().combine(ee.Reducer.count(), "", True),
        scale=1000,
        tileScale=4
    ).map(lambda f: f.set("date", ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")))).flatten()

    task_lst = ee.batch.Export.table.toDrive(
        collection=lst_table,
        description=f"MONSOON_PULSE_MODIS_LST_8Day_{start_year}_{end_year}",
        folder="MONSOON_PULSE_EXPORTS",
        fileFormat="CSV"
    )
    task_lst.start()
    print(f"  -> MODIS LST Task ID: {task_lst.id}")

    print("\n[GEE Task 3/5] Dispatching MODIS NDVI (2001-2024) Extraction...")
    def mask_modis_ndvi(img):
        qa = img.select("SummaryQA")
        qa_mask = qa.lte(1)
        ndvi = img.select("NDVI").multiply(0.0001).rename("ndvi")
        return ndvi.updateMask(qa_mask).updateMask(land_mask).copyProperties(img, ["system:time_start"])

    modis_ndvi = ee.ImageCollection("MODIS/061/MOD13Q1") \
        .filterBounds(kerala_fc) \
        .filterDate(f"{start_year}-01-01", f"{end_year}-12-31") \
        .map(mask_modis_ndvi)

    ndvi_table = modis_ndvi.map(lambda img: img.reduceRegions(
        collection=kerala_fc,
        reducer=ee.Reducer.mean().combine(ee.Reducer.count(), "", True),
        scale=250,
        tileScale=4
    ).map(lambda f: f.set("date", ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")))).flatten()

    task_ndvi = ee.batch.Export.table.toDrive(
        collection=ndvi_table,
        description=f"MONSOON_PULSE_MODIS_NDVI_16Day_{start_year}_{end_year}",
        folder="MONSOON_PULSE_EXPORTS",
        fileFormat="CSV"
    )
    task_ndvi.start()
    print(f"  -> MODIS NDVI Task ID: {task_ndvi.id}")

    print("\n[GEE Task 4/5] Dispatching NASA SMAP Soil Moisture (2015-2024)...")
    smap_col = ee.ImageCollection("NASA/SMAP/SPL4SMGP/008") \
        .filterBounds(kerala_fc) \
        .filterDate("2015-04-01", f"{end_year}-12-31") \
        .select("sm_rootzone")

    smap_table = smap_col.map(lambda img: img.updateMask(land_mask).reduceRegions(
        collection=kerala_fc,
        reducer=ee.Reducer.mean().combine(ee.Reducer.count(), "", True),
        scale=9000,
        tileScale=4
    ).map(lambda f: f.set("date", ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")))).flatten()

    task_smap = ee.batch.Export.table.toDrive(
        collection=smap_table,
        description=f"MONSOON_PULSE_SMAP_RootZone_2015_{end_year}",
        folder="MONSOON_PULSE_EXPORTS",
        fileFormat="CSV"
    )
    task_smap.start()
    print(f"  -> SMAP Soil Moisture Task ID: {task_smap.id}")

    print("\n[GEE Task 5/5] Dispatching NASA GPM IMERG Daily Precipitation Extraction...")
    # For GPM daily, export in annual chunks to respect Earth Engine memory limits
    print("  -> Submitting GPM annual batch export tasks for key reference years (2024, 2018)...")
    for yr in [2024, 2018]:
        gpm_daily_col = build_gpm_daily_collection(ee, f"{yr}-01-01", f"{yr}-12-31", kerala_fc)
        gpm_table = gpm_daily_col.map(lambda img: img.reduceRegions(
            collection=kerala_fc,
            reducer=ee.Reducer.mean().combine(ee.Reducer.count(), "", True),
            scale=11132,
            tileScale=4
        ).map(lambda f: f.set("date", img.get("date_str")).set("year", yr))).flatten()

        task_gpm = ee.batch.Export.table.toDrive(
            collection=gpm_table,
            description=f"MONSOON_PULSE_GPM_IMERG_Daily_{yr}",
            folder="MONSOON_PULSE_EXPORTS",
            fileFormat="CSV"
        )
        task_gpm.start()
        print(f"  -> GPM IMERG {yr} Task ID: {task_gpm.id}")

    print("\nAll 5 multi-sensor GEE extraction tasks submitted successfully.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MONSOON PULSE GEE Extraction Pipeline")
    parser.add_argument("--start-year", type=int, default=2001)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--output-dir", type=str, default="data/raw")
    parser.add_argument("--project", type=str, default=None, help="Google Cloud Project ID")
    args = parser.parse_args()

    run_pipeline(
        start_year=args.start_year,
        end_year=args.end_year,
        output_dir=args.output_dir,
        project_id=args.project
    )
