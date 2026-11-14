# MONSOON PULSE
### Satellite-Based Earth-System Trend Detection & Environmental Intelligence Platform
**Event:** NASA Space Apps Challenge 2026  
**Challenge Statement:** [Be An Earth System Trend Detective!](https://www.spaceappschallenge.org/2026/challenges/earth-system-trend-detective/)  
**Study Region:** Kerala, India (All 14 Administrative Districts)  
**Observation Window:** 2001–2024 (NASA SMAP: 2015–2024)  
**License:** [Apache 2.0 Open Source](LICENSE)  

---

## 1. Project Overview & Problem Statement

### The Problem
Regional Earth systems are dynamic, interconnected networks of atmospheric, hydrological, ecological, and geomorphological processes. Across vulnerable tropical coastal-mountain landscapes such as Kerala, India—flanked between the Arabian Sea and the steep escarpments of the Western Ghats—climate extremes and land-surface alterations interact in non-linear ways:
1. **Intensified Extreme Precipitation:** Regional rainfall extremes can surge in highland windward districts while declining or shifting in midland valleys.
2. **Thermal Channeling:** Land Surface Temperatures rise at different rates across urbanized coastal plains, the arid Palakkad mountain gap, and forested highlands.
3. **Soil Saturation Dynamics:** Root-zone moisture saturation acts as a primary trigger for flooding and catastrophic slope failures (such as the 2018 century flood and the 2024 Wayanad Chooralmala landslide disaster).
4. **Topographical Compounding:** Identical volumes of precipitation produce vastly different geomorphic exposure when falling on steep mountain slopes compared to coastal wetlands.

### Our Solution
**MONSOON PULSE** is an open-source, satellite-based Earth-system trend detection and environmental intelligence observatory. It ingests historical multi-sensor NASA Earth-observation records spanning 2001–2024 across Kerala's 14 administrative districts to systematically determine:
- **What is changing?** (Rainfall extremes, land surface heating, vegetation canopy greenness, root-zone soil water).
- **Where is it changing?** (District-by-district spatial gradients across coastal, midland, and highland zones).
- **How rapidly is it changing?** (Theil-Sen robust slope estimator with non-parametric 95% confidence intervals).
- **Are the trends statistically significant?** (Mann-Kendall monotonic trend tests with Yue & Wang autocorrelation variance correction and Benjamini-Hochberg False Discovery Rate control).
- **How do multiple variables behave together?** (Introduces two project-defined compound indicators: **HMV** and **RTE**).

---

## 2. NASA Earth-Observation Datasets

| Dataset | Sensor / Platform | Spatial Resolution | Temporal Frequency | GEE Collection Identifier | Parameter & Physical Units |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GPM IMERG V07** | NASA Global Precipitation Measurement | 0.1° (~10 km) | 30-min (Daily Integrated) | `NASA/GPM_L3/IMERG_V07` | Precipitation Rate ($mm/hr \rightarrow mm/day$) |
| **MODIS MOD11A2 V6.1** | Terra Land Surface Temperature | 1 km | 8-Day Composite | `MODIS/061/MOD11A2` | Daytime LST ($Kelvin \times 0.02 - 273.15 = ^\circ C$) |
| **MODIS MOD13Q1 V6.1** | Terra Vegetation Indices | 250 m | 16-Day Composite | `MODIS/061/MOD13Q1` | Canopy NDVI ($DN \times 0.0001$, range: -0.2 to 1.0) |
| **SMAP SPL4SMGP V008** | Soil Moisture Active Passive L4 | 9 km (EASE-Grid 2.0) | 3-Hourly Assimilated | `NASA/SMAP/SPL4SMGP/008` | Root-Zone Soil Moisture (0–100 cm depth, $m^3/m^3$) |
| **SRTMGL1 V003** | NASA/USGS Shuttle Radar Topography | 30 m (1 arc-sec) | Static Geomorphometry | `USGS/SRTMGL1_003` | Elevation ($m$) and Horn's Slope ($^\circ$) |

*Note on SMAP Temporal Availability:* Because NASA's SMAP mission launched in 2015, soil moisture time series and the 3-variable HMV composite are evaluated over the 2015–2024 common multi-sensor window, avoiding invalid historical backcasting.

---

## 3. Scientific Methodology & Formulations

### A. ETCCDI R95p Extreme Precipitation Index
Following Expert Team on Climate Change Detection and Indices (ETCCDI) protocols:
- **Wet Day Condition:** Daily precipitation $P_d \ge 1.0\text{ mm/day}$.
- **Baseline Reference Window:** 2001–2020 (standard 20-year climatological base).
- **95th Percentile ($P_{95}$):** Calculated strictly on baseline wet days.
- **Annual R95p:** Accumulated rainfall on wet days exceeding the reference 95th percentile:
  $$R95p = \sum_{d \in \text{wet days}, P_d > P_{95}} P_d\quad (\text{mm})$$
- **Seasonal JJAS R95p:** Same extreme threshold applied specifically to the June–September South-West monsoon window.

### B. HMV — Heat–Moisture–Vegetation Compound Indicator
Introduced to diagnose coupled thermal-moisture-vegetative stress across districts:
$$HMV = \frac{Z_{LST} - Z_{SMAP} - Z_{NDVI}}{3}$$
Where each variable is standardized as a $Z$-score ($Z_X = (X - \mu_{base}) / \sigma_{base}$) relative to the common multi-sensor period (2015–2024):
- **Positive HMV (> +0.5):** Elevated thermal stress coincident with soil moisture deficits and vegetation browning (e.g., during the 2016 severe regional drought).
- **Negative HMV (< -0.5):** Cool, moisture-rich, healthy vegetative equilibrium.

### C. RTE — Rainfall–Terrain Exposure Screening Indicator
Couples hydro-meteorological monsoon forcing with static geomorphological steepness:
$$RTE = Z_{R95p,JJAS} \times S_{norm}$$
Where:
- $Z_{R95p,JJAS}$ = Standardized June–September extreme rainfall anomaly.
- $S_{norm} = \frac{S_d - S_{min}}{S_{max} - S_{min}}$ = Min-Max normalized district mean terrain slope ($[0, 1]$) derived from NASA/USGS SRTM.
- *Scientific Disclaimer:* RTE is a geographical screening index identifying compound hydro-topographic exposure; it is not a direct deterministic prediction of landslide occurrence.

### D. Statistical Trend Testing Framework
- **Mann–Kendall Test:** Evaluates monotonic trends in non-normally distributed environmental time series. Tie-corrected variance $Var(S)$ and standardized $Z$-statistic.
- **Modified Mann–Kendall:** Incorporates Yue & Wang variance correction when lag-1 serial autocorrelation ($r_1$) exceeds Anderson 95% confidence limits.
- **Theil–Sen Estimator:** Calculates the median of all pairwise slopes $\beta = \text{median}\left(\frac{y_j - y_i}{x_j - x_i}\right)$, providing robustness against extreme outliers (e.g. 2018 flood).
- **Non-Parametric Confidence Intervals:** 95% rank-based confidence limits $[M_1, M_2]$ derived from Kendall's $Var(S)$.
- **Benjamini–Hochberg False Discovery Rate (FDR):** Controls family-wise error across all 70 simultaneous tests (14 districts $\times$ 5 environmental variables) at $\alpha = 0.05$:
  $$q_{(i)} = \min_{j \ge i} \left(\frac{m}{j} p_{(j)}\right)$$

---

## 4. Technical Architecture

```
NASA Earth-Observation Data Sources
[ GPM IMERG V07 • MODIS MOD11A2 • MODIS MOD13Q1 • SMAP SPL4SMGP • SRTMGL1 ]
                                │
                                ▼
         Google Earth Engine Satellite Processing Suite
         [ gee/gee_monsoon_pulse_extractor.js • gee/gee_monsoon_pulse_pipeline.py ]
         [ QA bitmask filtering • Spatial reducer • Unit conversions ]
                                │
                                ▼
         Data{Meet} Kerala 14 Districts Boundaries (ODbL / CC-BY)
         [ data/raw/kerala_districts.geojson ]
                                │
                                ▼
         Python Scientific Data Engineering & Quality Control
         [ src/ingestion: QualityAssuranceValidator, units_converter, dataset_loader ]
         [ Missing observation tracking • Physical plausibility checks ]
                                │
                                ▼
         Scientific Indices & Climatological Aggregation
         [ src/science: r95p_calculator, hmv_calculator, rte_calculator, temporal_aggregator ]
                                │
                                ▼
         Rigorous Statistical Testing Engine
         [ src/statistics: mann_kendall, theil_sen, autocorrelation, fdr_correction, sensitivity_tester ]
                                │
                                ▼
         Schema Validation & Structured Serialization
         [ src/export: schema_validator, dashboard_exporter ]
         [ Outputs: monsoon_pulse_dashboard_data.json, r95p, hmv, rte, fdr JSON artifacts ]
                                │
                                ▼
         Interactive Geospatial Observatory (React 19 + Tailwind + Recharts + Leaflet)
         [ frontend/src: 10 interactive modules, SVG choropleths, side-by-side district compare ]
```

---

## 5. Alignment with NASA Space Apps 2026 Judging Criteria

### 1. Impact
Provides an accessible, district-granular Earth-system observatory for Kerala, turning raw NASA satellite data into actionable environmental intelligence for climate scientists, disaster managers, researchers, and citizens.

### 2. Creativity
Pioneers the **HMV** compound index (unifying thermal, soil water, and vegetative stress) and the **RTE** screening indicator (coupling extreme monsoon precipitation directly with digital elevation slope steepness).

### 3. Validity
Built upon authentic NASA satellite products, ETCCDI climate extreme definitions, non-parametric Theil-Sen estimators, autocorrelation corrections, and Benjamini-Hochberg FDR multi-testing error control. Verified by 20 automated unit tests (100% pass rate).

### 4. Relevance
Directly addresses "Be An Earth System Trend Detective!":
- Identifies variables (Precipitation, LST, NDVI, Soil Moisture, Terrain).
- Acquires regional observations across Kerala's 14 districts.
- Evaluates long-term time series (2001–2024).
- Determines what is changing, where it is changing, and its rate of change.
- Evaluates statistical significance and uncertainty.

### 5. Presentation
Delivers a responsive, dark-mode satellite observatory web application with zero-login requirements, interactive SVG choropleths, 24-year comparative time-series charts, and a 30-second judge demonstration sequence.

---

## 6. 30-Second Judge Demonstration Script

| Time | Action / Screen | Narration / Scientific Highlight |
| :--- | :--- | :--- |
| **0–5s** | **Overview Tab** | "Welcome to MONSOON PULSE, an Earth-system trend observatory evaluating 24 years of satellite observations across Kerala's 14 districts." |
| **5–12s** | **Interactive Map** | "Switch between SRTM Terrain Slope and R95p Extreme Rain on our geospatial choropleth to visualize Kerala's steep Western Ghats escarpment." |
| **12–18s** | **Rainfall & Temperature** | "Inspect the GPM IMERG time series: notice the unprecedented R95p extreme rainfall spikes during the 2018 century flood and 2024 bursts, alongside a +0.28°C/decade warming rate." |
| **18–24s** | **HMV & RTE Explorers** | "Examine our compound indicators: HMV diagnosed the severe 2016 ecological drought, while RTE pinpoints extreme slope-precipitation exposure in Wayanad and Idukki." |
| **24–30s** | **Statistical Rigor Tab** | "All 70 trend hypotheses are evaluated with Mann-Kendall tests, Theil-Sen confidence intervals, and Benjamini-Hochberg FDR q-values—ensuring every finding is statistically credible." |

---

## 7. Installation & Reproducibility Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js v18+ (tested on Node v24.19 / npm 11.17)
- Git

### 1. Clone & Set Up Python Environment
```bash
# Clone the repository
git clone https://github.com/monsoon-pulse/monsoon-pulse.git
cd monsoon-pulse

# Install Python scientific dependencies
pip install -r requirements.txt
```

### 2. Run the Full Scientific Pipeline
```bash
# Ingest data, compute R95p, HMV, RTE, statistical tests, and export production JSON
python scripts/run_full_pipeline.py

# Run validation report generator
python scripts/generate_validation_report.py
```

### 3. Run Automated Tests
```bash
python -m pytest tests -v
```

### 4. Launch the Interactive Dashboard
```bash
# Enter frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# OR build and run production preview:
npm run build
npm run preview
```
Visit `http://localhost:5173` or `http://localhost:4173` in your browser.

---

## 8. Third-Party Attributions & Open Source Licensing

- **Code License:** [Apache License 2.0](LICENSE) (OSI-compliant).
- **Administrative Boundaries:** [Data{Meet} Maps Collection](https://github.com/datameet/maps) (Creative Commons Attribution 2.5 India / Open Data Commons ODbL).
- **Satellite Data Providers:**
  - NASA Goddard Space Flight Center (GPM IMERG V07)
  - NASA Land Processes Distributed Active Archive Center (MODIS MOD11A2 & MOD13Q1)
  - NASA National Snow and Ice Data Center (SMAP SPL4SMGP V008)
  - NASA Jet Propulsion Laboratory / USGS (SRTMGL1 V003)
  - Google Earth Engine Catalog
- **AI Usage Disclosure:** Software architecture, component engineering, and automated tests were developed with autonomous AI assistance in strict compliance with NASA Space Apps Challenge 2026 rules.

---

## 9. Final Submission Checklist

- [x] Clean-slate implementation built from the ground up.
- [x] Directly addresses "Be An Earth System Trend Detective!".
- [x] Ingests and processes all 5 specified NASA Earth-observation datasets.
- [x] Full Kerala regional scope (all 14 administrative districts).
- [x] 2001–2024 continuous historical observation period (SMAP: 2015–2024).
- [x] ETCCDI R95p extreme precipitation index fully implemented.
- [x] HMV compound indicator implemented with component Z-scores.
- [x] RTE screening indicator implemented with SRTM slope normalization.
- [x] Mann-Kendall, Theil-Sen, 95% CIs, autocorrelation, and FDR q-values calculated.
- [x] 10-section interactive web dashboard operational.
- [x] Zero-login access for judges.
- [x] Automated test suite passing with 100% pass rate.
- [x] Open-source license (Apache 2.0) and third-party attributions documented.
