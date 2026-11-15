# MONSOON PULSE — Google Earth Engine Satellite Extraction Suite
## NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

This directory provides the complete, reproducible Google Earth Engine (GEE) extraction pipeline for MONSOON PULSE across all 14 administrative districts of Kerala, India.

---

## 1. Earth Observation Datasets & Extraction Specifications

| Dataset | GEE Collection Identifier | Target Band | Native Spatial Res | Temporal Res | Processing & Quality Filters | Units |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NASA GPM IMERG V07** | `NASA/GPM_L3/IMERG_V07` | `precipitationCal` | 0.1° (~10 km) | Half-hourly | Rate &times; 0.5 hr, daily calendar sum | mm/day |
| **MODIS Terra LST V6.1** | `MODIS/061/MOD11A2` | `LST_Day_1km` | 1 km | 8-day composite | Scale 0.02, &minus;273.15, `QC_Day` bits 0-1 &le; 1, Land-masked | °C |
| **MODIS Terra NDVI V6.1** | `MODIS/061/MOD13Q1` | `NDVI` | 250 m | 16-day composite | Scale 0.0001, `SummaryQA` &le; 1 (Good/Marginal), Land-masked | Dimensionless |
| **NASA SMAP L4 V008** | `NASA/SMAP/SPL4SMGP/008`| `sm_rootzone` | 9 km (EASE-Grid 2.0) | 3-hourly | Daily mean composite, Land-masked | m³/m³ |
| **NASA/USGS SRTMGL1 V003** | `USGS/SRTMGL1_003` | `elevation` | 30 m (1 arc-sec) | Static baseline | Horn slope algorithm (`ee.Terrain.slope`) | meters / degrees |

---

## 2. Spatial Aggregation Methodology & Quality Masking

To ensure scientific credibility across heterogeneous spatial resolutions (from 30m SRTM to 10km GPM IMERG):

1. **District Boundary Intersection:**
   - Kerala's 14 administrative district polygons are loaded from the official Survey of India / FAO GAUL level-2 collection.
   - Spatial reduction is performed via `reduceRegions` using `ee.Reducer.mean()` combined with `ee.Reducer.count()`.
2. **Area Weighting & Partial Pixel Overlap:**
   - Google Earth Engine's default vector-raster intersection computes fractional pixel overlaps automatically at the specified reduction `scale`.
   - Native raster scales are respected: SRTM at 30 m, MODIS NDVI at 250 m, MODIS LST at 1,000 m, SMAP at 9,000 m, and GPM at 11,132 m.
3. **Coastal & Mixed Land-Water Masking:**
   - Kerala has 590 km of coastline bordering the Arabian Sea and large coastal lagoons (e.g., Vembanad Lake in Alappuzha/Ernakulam).
   - A high-resolution SRTM land mask (`elevation >= -5m`) is applied to MODIS and SMAP collections to mask out ocean/marine water pixels, preventing open-water thermal inertia or reflectance from contaminating district terrestrial means.
4. **Invalid Pixel Tracking:**
   - Cloud-contaminated or poor-quality pixels identified by MODIS QA flags (`QC_Day` > 1 or `SummaryQA` > 1) are masked out before spatial aggregation.
   - The reducer records both the area-weighted mean and the valid pixel count for every timestamp.

---

## 3. Daily Precipitation Aggregation Formulation

NASA GPM IMERG V07 provides calibrated precipitation rates in millimeters per hour (`mm/hr`) every 30 minutes (48 scenes per day).

$$\text{Precipitation}_{\text{daily}} = \sum_{t=1}^{48} \left( \text{rate}_t \times 0.5 \text{ hr} \right)$$

In `gee_monsoon_pulse_extractor.js`, calendar days are sequentially generated. For each day, all 48 half-hourly scenes are filtered, multiplied by $0.5$, and summed with `ee.Reducer.sum()` into a true daily accumulation image (mm/day).

---

## 4. Execution Instructions

### Option A: Google Earth Engine Code Editor (Zero Setup)
1. Open [Google Earth Engine Code Editor](https://code.earthengine.google.com/).
2. Copy the entire contents of [`gee/gee_monsoon_pulse_extractor.js`](./gee_monsoon_pulse_extractor.js).
3. Paste into the Code Editor script pane and click **Run**.
4. The visual interactive map will render Kerala's districts, SRTM terrain slope, LST climatology, NDVI greenness, and SMAP soil moisture.
5. In the **Tasks** tab, click **Run** on any registered export tasks to save district time series CSVs directly to Google Drive.

### Option B: Python API Automated Extraction
1. Ensure the Earth Engine API is installed: `pip install earthengine-api`
2. Authenticate: `earthengine authenticate`
3. Execute the automated batch pipeline:
   ```bash
   python gee/gee_monsoon_pulse_pipeline.py --project <YOUR_GEE_PROJECT_ID>
   ```
