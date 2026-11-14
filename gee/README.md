# MONSOON PULSE — Google Earth Engine (GEE) Satellite Extraction Suite
## NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

This directory contains the satellite extraction workflows that query and reduce NASA Earth-observation datasets across Kerala's 14 administrative districts.

---

## 1. Datasets Queried

| Parameter | Sensor / Collection | Resolution | Temporal Frequency | GEE Collection Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Precipitation** | NASA GPM IMERG V07 Final Run | 0.1° (~10 km) | 30-min (aggregated to Daily) | `NASA/GPM_L3/IMERG_V07` |
| **Land Surface Temperature** | MODIS Terra MOD11A2 V6.1 | 1 km | 8-Day Composite | `MODIS/061/MOD11A2` |
| **Vegetation Index (NDVI)** | MODIS Terra MOD13Q1 V6.1 | 250 m | 16-Day Composite | `MODIS/061/MOD13Q1` |
| **Root-Zone Soil Moisture** | NASA SMAP SPL4SMGP V008 | 9 km | 3-Hourly Assimilated | `NASA/SMAP/SPL4SMGP/008` |
| **Elevation & Terrain Slope** | NASA/USGS SRTMGL1 V003 | 30 m (1 arc-sec) | Static DEM Baseline | `USGS/SRTMGL1_003` |

---

## 2. Quality Assurance & Filtering Rules

### MODIS Land Surface Temperature (MOD11A2)
- Band: `LST_Day_1km`
- QC Band: `QC_Day`
- Filter: Bits 0–1 of `QC_Day` must equal `00` (LST produced, good quality) or `01` (produced, other quality). Pixels flagged with `10` or `11` (clouds or unproduced) are masked.
- Scale Factor: $0.02$
- Unit Conversion: $T_{Celsius} = (LST_{raw} \times 0.02) - 273.15$

### MODIS Vegetation Indices (MOD13Q1)
- Band: `NDVI`
- QC Band: `SummaryQA`
- Filter: `SummaryQA <= 1` (0 = Good data, 1 = Marginal data). Clouds (3) and snow/ice (2) are masked.
- Scale Factor: $0.0001$
- Valid Range: $-0.2$ to $+1.0$

### NASA GPM IMERG V07 Precipitation
- Band: `precipitation`
- Unit: $mm/hr$
- Daily Accumulation: Sum of 48 half-hourly time intervals:
  $$\text{Daily Rainfall (mm)} = \sum_{t=1}^{48} (\text{precipitation}_t \times 0.5)$$
- Wet-day condition: $\text{Daily Rainfall} \ge 1.0\text{ mm}$

### NASA SMAP L4 Root-Zone Soil Moisture
- Band: `sm_rootzone`
- Units: $m^3/m^3$ (volumetric water content)
- Period: 2015-04-01 to 2024-12-31 (reflecting launch and operational availability)

### NASA/USGS SRTM Terrain Slope
- Band: `elevation` (m)
- Terrain Slope: Computed using Horn's algorithm via `ee.Terrain.slope(elevation)` in degrees.
- Aggregation: District mean slope ($S$) and 90th percentile slope ($S_{90}$).

---

## 3. How to Run

### Option A: Google Earth Engine Code Editor (Interactive Web GUI)
1. Open the [Google Earth Engine Code Editor](https://code.earthengine.google.com/).
2. Copy and paste the contents of `gee_monsoon_pulse_extractor.js` into the Code Editor script pane.
3. Click **Run** to visualize Kerala's terrain, rainfall gradients, LST thermal hotspots, and SMAP soil moisture layers.
4. In the **Tasks** tab on the right panel, click **Run** on the export tasks to export CSVs directly to your Google Drive (`MONSOON_PULSE_DATA/`).

### Option B: Automated Python Batch Pipeline
1. Ensure `earthengine-api` is installed:
   ```bash
   pip install earthengine-api
   ```
2. Authenticate your Google Earth Engine account:
   ```bash
   earthengine authenticate
   ```
3. Execute the extraction script:
   ```bash
   python gee/gee_monsoon_pulse_pipeline.py --start-year 2001 --end-year 2024 --output-dir data/raw
   ```
