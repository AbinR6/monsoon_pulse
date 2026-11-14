/**
 * MONSOON PULSE — Google Earth Engine Code Editor Extraction Suite
 * NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
 * 
 * Study Region: Kerala, India (14 Districts)
 * Observation Period: 2001–2024 (SMAP: 2015–2024)
 * 
 * Datasets:
 * 1. NASA GPM IMERG V07: NASA/GPM_L3/IMERG_V07 (Precipitation, 0.1°, 30-min)
 * 2. MODIS MOD11A2 V6.1: MODIS/061/MOD11A2 (LST, 1km, 8-day)
 * 3. MODIS MOD13Q1 V6.1: MODIS/061/MOD13Q1 (NDVI, 250m, 16-day)
 * 4. NASA SMAP L4 V008: NASA/SMAP/SPL4SMGP/008 (Root-Zone Soil Moisture, 9km, 3-hourly)
 * 5. NASA/USGS SRTM V003: USGS/SRTMGL1_003 (Elevation & Slope, 30m)
 */

// 1. REGIONAL BOUNDARIES — KERALA DISTRICTS
// Load Kerala administrative boundary from FAO GAUL / LSIB / custom FeatureCollection
var kerala = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kerala'));

// Center map on Kerala
Map.centerObject(kerala, 8);
Map.setOptions('HYBRID');

// Styling for districts
var districtOutline = ee.Image().paint({
  featureCollection: kerala,
  color: 1,
  width: 2
});
Map.addLayer(districtOutline, {palette: ['#FFFFFF']}, 'Kerala District Outlines', true);

// 2. NASA/USGS SRTM V003 — ELEVATION & TERRAIN SLOPE
var srtm = ee.Image('USGS/SRTMGL1_003').clip(kerala);
var elevation = srtm.select('elevation');
var slope = ee.Terrain.slope(elevation);

var elevVis = {min: 0, max: 2500, palette: ['#1a9850', '#91cf60', '#d9ef8b', '#fee08b', '#fc8d59', '#d73027']};
var slopeVis = {min: 0, max: 45, palette: ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#31a354', '#006d2c']};

Map.addLayer(elevation, elevVis, 'SRTM Elevation (m)', false);
Map.addLayer(slope, slopeVis, 'Terrain Slope (degrees)', true);

// 3. NASA GPM IMERG V07 — PRECIPITATION (2001–2024)
// Daily rainfall is aggregated by summing half-hourly precipitation rates: rate (mm/hr) * 0.5 hr
function getDailyPrecip(startDate, endDate) {
  var imergCol = ee.ImageCollection('NASA/GPM_L3/IMERG_V07')
    .filterBounds(kerala)
    .filterDate(startDate, endDate)
    .select('precipitation'); // mm/hr

  // Aggregate half-hourly rates to daily sum: rate * 0.5 hr
  var dailyCol = imergCol.map(function(img) {
    var dailyMm = img.multiply(0.5).rename('precip_mm');
    return dailyMm.copyProperties(img, ['system:time_start']);
  });
  return dailyCol;
}

// 4. MODIS MOD11A2 V6.1 — LAND SURFACE TEMPERATURE (8-DAY)
// Scale: 0.02, Convert Kelvin to Celsius: (K * 0.02) - 273.15
function maskModisLst(image) {
  var qa = image.select('QC_Day');
  // Bits 0-1: Mandatory QA flags (00 = LST produced, good quality; 01 = produced, check other QA)
  var qaMask = qa.bitwiseAnd(3).lte(1);
  var lstCelsius = image.select('LST_Day_1km')
    .multiply(0.02)
    .subtract(273.15)
    .rename('LST_Day_Celsius');
  return lstCelsius.updateMask(qaMask).copyProperties(image, ['system:time_start']);
}

var modisLstCol = ee.ImageCollection('MODIS/061/MOD11A2')
  .filterBounds(kerala)
  .filterDate('2001-01-01', '2024-12-31')
  .map(maskModisLst);

var lstVis = {min: 20, max: 40, palette: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#fdae61', '#f46d43', '#d73027']};
Map.addLayer(modisLstCol.mean().clip(kerala), lstVis, 'Mean LST Day (°C) 2001-2024', false);

// 5. MODIS MOD13Q1 V6.1 — VEGETATION INDICES (NDVI 16-DAY)
// Scale: 0.0001, QA Filter: SummaryQA <= 1 (Good or Marginal)
function maskModisNdvi(image) {
  var qa = image.select('SummaryQA');
  var qaMask = qa.lte(1); // 0 = Good, 1 = Marginal
  var ndvi = image.select('NDVI')
    .multiply(0.0001)
    .rename('NDVI');
  return ndvi.updateMask(qaMask).copyProperties(image, ['system:time_start']);
}

var modisNdviCol = ee.ImageCollection('MODIS/061/MOD13Q1')
  .filterBounds(kerala)
  .filterDate('2001-01-01', '2024-12-31')
  .map(maskModisNdvi);

var ndviVis = {min: 0.1, max: 0.85, palette: ['#8c510a', '#d8b365', '#f6e8c3', '#c7eae5', '#5ab4ac', '#01665e']};
Map.addLayer(modisNdviCol.mean().clip(kerala), ndviVis, 'Mean NDVI 2001-2024', false);

// 6. NASA SMAP L4 V008 — ROOT-ZONE SOIL MOISTURE (2015–2024)
// Units: m^3/m^3 volumetric soil moisture
var smapCol = ee.ImageCollection('NASA/SMAP/SPL4SMGP/008')
  .filterBounds(kerala)
  .filterDate('2015-04-01', '2024-12-31')
  .select('sm_rootzone');

var smapVis = {min: 0.1, max: 0.45, palette: ['#edf8fb', '#b2e2e2', '#66c2a4', '#2ca25f', '#006d2c']};
Map.addLayer(smapCol.mean().clip(kerala), smapVis, 'Mean Root-Zone Soil Moisture 2015-2024', false);

// 7. DISTRICT-LEVEL SPATIAL REDUCTION & EXPORT DEFINITIONS
// Compute terrain summary metrics per district
var terrainStats = slope.addBands(elevation).reduceRegions({
  collection: kerala,
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.percentile([90]),
    sharedInputs: true
  }),
  scale: 30
});

Export.table.toDrive({
  collection: terrainStats,
  description: 'Kerala_Districts_SRTM_Terrain_Stats',
  folder: 'MONSOON_PULSE_DATA',
  fileFormat: 'CSV'
});

print('MONSOON PULSE GEE extraction initialized.');
print('Districts loaded:', kerala.size());
