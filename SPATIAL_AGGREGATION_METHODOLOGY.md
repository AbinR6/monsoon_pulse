# MONSOON PULSE — Spatial Aggregation Methodology & Quality Protocol
## NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

This document provides a formal scientific specification of the spatial aggregation methods, boundary intersection mechanics, coastal water masking, and pixel validity tracking implemented across the MONSOON PULSE platform.

---

## 1. Multi-Resolution Harmonization Framework

MONSOON PULSE ingests Earth-observation datasets spanning over two orders of magnitude in native spatial resolution:

| Sensor / Dataset | Native Spatial Resolution | Scale Parameter in GEE | Aggregation Reducer |
| :--- | :--- | :--- | :--- |
| **NASA/USGS SRTMGL1 V003** | 30 meters (1 arc-second) | 30 m | Area-weighted Mean, Min, Max, P10, P90 |
| **MODIS MOD13Q1 V6.1 (NDVI)**| 250 meters | 250 m | Quality-masked Area-weighted Mean |
| **MODIS MOD11A2 V6.1 (LST)** | 1,000 meters (1 km) | 1,000 m | Quality-masked Area-weighted Mean |
| **NASA SMAP SPL4SMGP V008** | 9,000 meters (9 km EASE-Grid 2.0) | 9,000 m | Land-masked Area-weighted Mean |
| **NASA GPM IMERG V07** | 0.1° (~11,132 meters) | 11,132 m | Daily-summed Area-weighted Mean |

---

## 2. Technical Answers to Core Spatial Aggregation Questions

### Q1: Are pixels averaged using their geographic intersection with district boundaries?
**Yes.** All spatial reductions are performed using geographic vector boundaries representing Kerala's 14 administrative districts (Survey of India / FAO GAUL level-2 polygons). Each raster pixel is evaluated against the vector geometry of the target district polygon.

### Q2: Are partial pixels weighted by their intersected area?
**Yes.** In Google Earth Engine's `reduceRegions` engine, when an image reduction is executed at the dataset's native scale, boundary pixels intersecting the district perimeter are assigned weights proportional to their fractional area of overlap:
$$\bar{X}_{\text{district}} = \frac{\sum_{i=1}^M w_i \cdot x_i}{\sum_{i=1}^M w_i}$$
where $w_i \in (0, 1]$ represents the fraction of pixel $i$ falling strictly inside the district boundary, and $x_i$ is the valid pixel value.

### Q3: Are invalid pixels excluded before spatial averaging?
**Yes.** All satellite quality control flags are applied *prior* to spatial reduction:
- **MODIS LST:** Pixels where `QC_Day` bits 0–1 > 1 (indicating missing, cloud-covered, or poor-quality retrievals) are masked out (`updateMask`).
- **MODIS NDVI:** Pixels with `SummaryQA` > 1 (cloud-covered or snow/ice) are masked out.
- **SMAP Soil Moisture:** Retrieval error flags and frozen soil flags are masked out.
- Unmasked valid pixels are counted via `ee.Reducer.count()`, and the valid pixel fraction is monitored. If valid coverage over a district falls below 50% for a given composite scene, the observation is flagged.

### Q4: Is the district mean area-weighted?
**Yes.** Because geographic coordinates in WGS84 (EPSG:4326) vary slightly in linear distance across latitude, reductions are executed with the native projected resolution (e.g. 1000m for MODIS sinusoidal grid, 9km for SMAP cylindrical EASE-Grid 2.0), ensuring that each square kilometer of terrain contributes equal weight to the district mean.

### Q5: How are coastal pixels and mixed land-water pixels handled?
**Land-Sea Masking:**
- Kerala has 590 km of coastline bordering the Arabian Sea, as well as extensive coastal wetland and backwater networks (e.g., the Vembanad Lake delta in Alappuzha and Ernakulam).
- A high-resolution SRTM elevation and land-water mask (`elevation >= -5m`) is applied to all MODIS LST, NDVI, and SMAP images before district reduction.
- This prevents offshore open-water pixels (which have high thermal heat capacity and low reflectance) from artificially depressing daytime land-surface temperatures or corrupting vegetation indices in narrow coastal districts such as **Alappuzha**, **Kollam**, and **Ernakulam**.

---

## 3. District-Specific Physiographic Considerations

| District | Physiographic Zone | Spatial Aggregation Sensitivity | Treatment Protocol |
| :--- | :--- | :--- | :--- |
| **Alappuzha** | Coastal Lowland / Deltaic | High coastal perimeter, parts below sea level (Kuttanad) | High-res land mask isolates terrestrial rice paddies from marine pixels |
| **Idukki** | Highland Western Ghats | Extreme terrain relief (0 to 2,695m Anamudi) | High-density SRTM 30m grid captures slope variances; elevation-stratified reduction |
| **Wayanad** | Highland Plateau | Steep windward escarpments (average elevation ~750m) | Orographic gradient captured at 250m NDVI and 1km LST; GPM 10km grid captures mountain crest |
| **Palakkad** | Inland Valley / Gap | Low-elevation mountain breach (Palakkad Gap) | Thermal channeling captured at 1km MODIS resolution without boundary spillover into Tamil Nadu |
