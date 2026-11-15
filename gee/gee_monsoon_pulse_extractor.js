/**
 * MONSOON PULSE — Complete Google Earth Engine Extraction & Processing Suite
 * NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
 * 
 * Study Region: Kerala, India (14 Administrative Districts)
 * Observation Period: 2001–2024 (SMAP: 2015–2024)
 * 
 * Datasets Integrated:
 * 1. NASA GPM IMERG V07: NASA/GPM_L3/IMERG_V07 (Precipitation, 0.1°, 30-min -> Daily Sum)
 * 2. MODIS MOD11A2 V6.1: MODIS/061/MOD11A2 (Daytime LST, 1km, 8-day composite)
 * 3. MODIS MOD13Q1 V6.1: MODIS/061/MOD13Q1 (NDVI Vegetation Index, 250m, 16-day composite)
 * 4. NASA SMAP SPL4SMGP V008: NASA/SMAP/SPL4SMGP/008 (Root-Zone Soil Moisture, 9km, 3-hourly -> Daily Mean)
 * 5. NASA/USGS SRTMGL1 V003: USGS/SRTMGL1_003 (Elevation & Slope, 30m baseline)
 */

// ==============================================================================
// 1. REGIONAL BOUNDARIES & SPATIAL AGGREGATION MASK
// ==============================================================================

// Official Kerala administrative boundaries (14 districts)
// Sourced from FAO GAUL / Survey of India boundary definitions
var keralaDistricts = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kerala'));

// High-resolution land mask from SRTM to exclude open marine/water pixels
// prevents Arabian Sea water pixels from biasing coastal district LST/NDVI averages
var srtmLand = ee.Image('USGS/SRTMGL1_003').select('elevation');
var landMask = srtmLand.gte(-5); // Land elevation above -5m

Map.centerObject(keralaDistricts, 8);
Map.setOptions('HYBRID');

var districtOutline = ee.Image().paint({
  featureCollection: keralaDistricts,
  color: 1,
  width: 2
});
Map.addLayer(districtOutline, {palette: ['#00FFFF']}, 'Kerala 14 Districts', true);


// ==============================================================================
// 2. NASA/USGS SRTM V003 — 30m ELEVATION & TERRAIN SLOPE
// ==============================================================================

var srtm = ee.Image('USGS/SRTMGL1_003').clip(keralaDistricts);
var elevation = srtm.select('elevation').rename('elevation_m');
var slope = ee.Terrain.slope(elevation).rename('slope_deg');

var terrainCombined = elevation.addBands(slope);

// Area-weighted spatial reduction across districts with pixel count
var terrainStats = terrainCombined.reduceRegions({
  collection: keralaDistricts,
  reducer: ee.Reducer.mean()
    .combine(ee.Reducer.minMax(), '', true)
    .combine(ee.Reducer.percentile([10, 90]), '', true)
    .combine(ee.Reducer.count(), '', true),
  scale: 30,
  tileScale: 4
});

Export.table.toDrive({
  collection: terrainStats,
  description: 'MONSOON_PULSE_SRTM_Terrain_Stats_14Districts',
  folder: 'MONSOON_PULSE_EXPORTS',
  fileFormat: 'CSV',
  selectors: ['ADM2_NAME', 'elevation_m_mean', 'elevation_m_min', 'elevation_m_max', 'elevation_m_p90', 'slope_deg_mean', 'slope_deg_min', 'slope_deg_max', 'slope_deg_p90', 'count']
});


// ==============================================================================
// 3. NASA GPM IMERG V07 — DAILY ACCUMULATED PRECIPITATION (2001–2024)
// ==============================================================================
// GPM IMERG V07 provides half-hourly calibrated precipitation rate ('precipitationCal') in mm/hr.
// To compute exact daily total (mm/day):
// Multiply each 30-min image by 0.5 hours, group all images by calendar day, and sum.

function exportGpmDailyForYear(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31).advance(1, 'day');
  var nDays = end.difference(start, 'day');
  var daySequence = ee.List.sequence(0, nDays.subtract(1));

  var imergHalfHourly = ee.ImageCollection('NASA/GPM_L3/IMERG_V07')
    .filterBounds(keralaDistricts)
    .filterDate(start, end)
    .select('precipitationCal');

  var dailyImages = daySequence.map(function(d) {
    var dayStart = start.advance(d, 'day');
    var dayEnd = dayStart.advance(1, 'day');
    var slice = imergHalfHourly.filterDate(dayStart, dayEnd);

    // Sum 30-minute depths: rate (mm/hr) * 0.5 hr
    var dailyPrecip = slice.map(function(img) {
      return img.multiply(0.5);
    }).reduce(ee.Reducer.sum()).rename('precipitation_mm');

    return dailyPrecip
      .set('system:time_start', dayStart.millis())
      .set('date_str', dayStart.format('YYYY-MM-dd'))
      .set('year', year);
  });

  var dailyCol = ee.ImageCollection.fromImages(dailyImages);

  // Map spatial reduction over each day for each district
  var districtDailyTable = dailyCol.map(function(img) {
    var dateString = img.get('date_str');
    var reduced = img.reduceRegions({
      collection: keralaDistricts,
      reducer: ee.Reducer.mean().combine(ee.Reducer.count(), '', true),
      scale: 11132, // ~0.1 degree native resolution
      tileScale: 4
    });
    return reduced.map(function(feat) {
      return feat.set('date', dateString).set('year', year);
    });
  }).flatten();

  Export.table.toDrive({
    collection: districtDailyTable,
    description: 'MONSOON_PULSE_GPM_IMERG_Daily_' + year,
    folder: 'MONSOON_PULSE_EXPORTS',
    fileFormat: 'CSV',
    selectors: ['ADM2_NAME', 'date', 'year', 'mean', 'count']
  });
}

// Queue GPM daily exports for sample year (expand loop for 2001-2024 batch)
exportGpmDailyForYear(2024);
exportGpmDailyForYear(2018);


// ==============================================================================
// 4. MODIS MOD11A2 V6.1 — 8-DAY LAND SURFACE TEMPERATURE (2001–2024)
// ==============================================================================
// Band: LST_Day_1km, Scale: 0.02, Offset: -273.15 (°C)
// QC_Day: bits 0-1 (mandatory QA flags == 0 or 1, good quality)

function processModisLst(image) {
  var qc = image.select('QC_Day');
  var qaMask = qc.bitwiseAnd(3).lte(1); // Good / marginal quality
  var lstC = image.select('LST_Day_1km')
    .multiply(0.02)
    .subtract(273.15)
    .rename('lst_day_celsius');

  return lstC.updateMask(qaMask).updateMask(landMask)
    .copyProperties(image, ['system:time_start']);
}

var modisLst = ee.ImageCollection('MODIS/061/MOD11A2')
  .filterBounds(keralaDistricts)
  .filterDate('2001-01-01', '2024-12-31')
  .map(processModisLst);

var lstDistrictTimeseries = modisLst.map(function(img) {
  var dateStr = ee.Date(img.get('system:time_start')).format('YYYY-MM-dd');
  var reduced = img.reduceRegions({
    collection: keralaDistricts,
    reducer: ee.Reducer.mean().combine(ee.Reducer.count(), '', true),
    scale: 1000,
    tileScale: 4
  });
  return reduced.map(function(feat) {
    return feat.set('date', dateStr);
  });
}).flatten();

Export.table.toDrive({
  collection: lstDistrictTimeseries,
  description: 'MONSOON_PULSE_MODIS_LST_8Day_2001_2024',
  folder: 'MONSOON_PULSE_EXPORTS',
  fileFormat: 'CSV',
  selectors: ['ADM2_NAME', 'date', 'mean', 'count']
});


// ==============================================================================
// 5. MODIS MOD13Q1 V6.1 — 16-DAY VEGETATION INDEX (NDVI) (2001–2024)
// ==============================================================================
// Band: NDVI, Scale: 0.0001
// SummaryQA: 0 = Good data, 1 = Marginal data

function processModisNdvi(image) {
  var qa = image.select('SummaryQA');
  var qaMask = qa.lte(1);
  var ndvi = image.select('NDVI')
    .multiply(0.0001)
    .rename('ndvi');

  return ndvi.updateMask(qaMask).updateMask(landMask)
    .copyProperties(image, ['system:time_start']);
}

var modisNdvi = ee.ImageCollection('MODIS/061/MOD13Q1')
  .filterBounds(keralaDistricts)
  .filterDate('2001-01-01', '2024-12-31')
  .map(processModisNdvi);

var ndviDistrictTimeseries = modisNdvi.map(function(img) {
  var dateStr = ee.Date(img.get('system:time_start')).format('YYYY-MM-dd');
  var reduced = img.reduceRegions({
    collection: keralaDistricts,
    reducer: ee.Reducer.mean().combine(ee.Reducer.count(), '', true),
    scale: 250,
    tileScale: 4
  });
  return reduced.map(function(feat) {
    return feat.set('date', dateStr);
  });
}).flatten();

Export.table.toDrive({
  collection: ndviDistrictTimeseries,
  description: 'MONSOON_PULSE_MODIS_NDVI_16Day_2001_2024',
  folder: 'MONSOON_PULSE_EXPORTS',
  fileFormat: 'CSV',
  selectors: ['ADM2_NAME', 'date', 'mean', 'count']
});


// ==============================================================================
// 6. NASA SMAP SPL4SMGP V008 — ROOT-ZONE SOIL MOISTURE (2015–2024)
// ==============================================================================
// Band: sm_rootzone (0–100 cm depth, m^3/m^3 volumetric fraction)
// SMAP Science operations commence April 2015

function exportSmapDailyForYear(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31).advance(1, 'day');
  var nDays = end.difference(start, 'day');
  var daySequence = ee.List.sequence(0, nDays.subtract(1));

  var smapCol = ee.ImageCollection('NASA/SMAP/SPL4SMGP/008')
    .filterBounds(keralaDistricts)
    .filterDate(start, end)
    .select('sm_rootzone');

  var dailyImages = daySequence.map(function(d) {
    var dayStart = start.advance(d, 'day');
    var dayEnd = dayStart.advance(1, 'day');
    var dailyMean = smapCol.filterDate(dayStart, dayEnd)
      .mean()
      .updateMask(landMask)
      .rename('soil_moisture_m3_m3');

    return dailyMean
      .set('system:time_start', dayStart.millis())
      .set('date_str', dayStart.format('YYYY-MM-dd'))
      .set('year', year);
  });

  var smapDailyCol = ee.ImageCollection.fromImages(dailyImages);

  var districtSmapTable = smapDailyCol.map(function(img) {
    var dateString = img.get('date_str');
    var reduced = img.reduceRegions({
      collection: keralaDistricts,
      reducer: ee.Reducer.mean().combine(ee.Reducer.count(), '', true),
      scale: 9000,
      tileScale: 4
    });
    return reduced.map(function(feat) {
      return feat.set('date', dateString).set('year', year);
    });
  }).flatten();

  Export.table.toDrive({
    collection: districtSmapTable,
    description: 'MONSOON_PULSE_SMAP_RootZone_Daily_' + year,
    folder: 'MONSOON_PULSE_EXPORTS',
    fileFormat: 'CSV',
    selectors: ['ADM2_NAME', 'date', 'year', 'mean', 'count']
  });
}

// Queue SMAP exports for key test years
exportSmapDailyForYear(2024);
exportSmapDailyForYear(2018);

print('MONSOON PULSE complete multi-sensor extraction pipeline configured.');
print('All 5 dataset extraction and export tasks registered.');
