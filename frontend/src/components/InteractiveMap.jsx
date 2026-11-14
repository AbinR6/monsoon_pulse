import React, { useState, useMemo } from 'react';
import { Layers, Info, MapPin } from 'lucide-react';

export default function InteractiveMap({ 
  geoJsonData, 
  districtsData, 
  selectedDistrict, 
  onSelectDistrict 
}) {
  const [metric, setMetric] = useState('slope');
  const [hoveredDistrict, setHoveredDistrict] = useState(null);

  const metricConfigs = {
    slope: {
      label: 'Terrain Slope',
      unit: '°',
      getValue: (d) => d?.metadata?.mean_slope_deg ?? 0,
      getColor: (val) => {
        // 0 to 20 deg
        if (val > 15) return '#dc2626'; // Red (very steep)
        if (val > 10) return '#ea580c'; // Orange
        if (val > 6) return '#ca8a04';  // Yellow-amber
        if (val > 3) return '#16a34a';  // Green
        return '#0284c7';              // Blue (flat coast)
      },
      legend: ['< 3° (Coast)', '3–6°', '6–10° (Midland)', '10–15°', '> 15° (High Ghats)'],
      colors: ['#0284c7', '#16a34a', '#ca8a04', '#ea580c', '#dc2626']
    },
    elevation: {
      label: 'Elevation',
      unit: 'm',
      getValue: (d) => d?.metadata?.mean_elevation_m ?? 0,
      getColor: (val) => {
        if (val > 800) return '#7f1d1d'; // Deep red/brown
        if (val > 300) return '#c2410c';
        if (val > 120) return '#d97706';
        if (val > 50) return '#65a30d';
        return '#0284c7';
      },
      legend: ['< 50m (Lowland)', '50–120m', '120–300m', '300–800m', '> 800m (Highland)'],
      colors: ['#0284c7', '#65a30d', '#d97706', '#c2410c', '#7f1d1d']
    },
    r95p: {
      label: 'R95p Extreme Rain',
      unit: 'mm',
      getValue: (d) => {
        const lastYear = d?.annual_time_series?.[d.annual_time_series.length - 1];
        return lastYear?.r95p_annual_mm ?? 0;
      },
      getColor: (val) => {
        if (val > 1400) return '#1e1b4b'; // Deep Indigo
        if (val > 1100) return '#312e81';
        if (val > 800) return '#2563eb';
        if (val > 500) return '#0ea5e9';
        return '#bae6fd';
      },
      legend: ['< 500 mm', '500–800 mm', '800–1100 mm', '1100–1400 mm', '> 1400 mm'],
      colors: ['#bae6fd', '#0ea5e9', '#2563eb', '#312e81', '#1e1b4b']
    },
    lst: {
      label: 'Land Surface Temp',
      unit: '°C',
      getValue: (d) => {
        const lastYear = d?.annual_time_series?.[d.annual_time_series.length - 1];
        return lastYear?.lst_celsius ?? 0;
      },
      getColor: (val) => {
        if (val > 34) return '#b91c1c'; // Red
        if (val > 32) return '#ea580c'; // Orange
        if (val > 30) return '#d97706'; // Amber
        if (val > 27) return '#059669'; // Emerald
        return '#0284c7';              // Cool blue
      },
      legend: ['< 27°C (Highlands)', '27–30°C', '30–32°C', '32–34°C', '> 34°C (Thermal Gap)'],
      colors: ['#0284c7', '#059669', '#d97706', '#ea580c', '#b91c1c']
    },
    ndvi: {
      label: 'Vegetation (NDVI)',
      unit: '',
      getValue: (d) => {
        const lastYear = d?.annual_time_series?.[d.annual_time_series.length - 1];
        return lastYear?.ndvi ?? 0;
      },
      getColor: (val) => {
        if (val > 0.75) return '#064e3b'; // Dense green
        if (val > 0.68) return '#047857';
        if (val > 0.60) return '#10b981';
        if (val > 0.52) return '#a7f3d0';
        return '#fde68a';
      },
      legend: ['< 0.52', '0.52–0.60', '0.60–0.68', '0.68–0.75', '> 0.75 (Evergreen)'],
      colors: ['#fde68a', '#a7f3d0', '#10b981', '#047857', '#064e3b']
    },
    rte: {
      label: 'RTE Exposure Index',
      unit: '',
      getValue: (d) => {
        const lastYear = d?.annual_time_series?.[d.annual_time_series.length - 1];
        return lastYear?.rte ?? 0;
      },
      getColor: (val) => {
        if (val > 0.7) return '#7f1d1d';
        if (val > 0.3) return '#c2410c';
        if (val > 0.0) return '#eab308';
        if (val > -0.4) return '#0284c7';
        return '#3b82f6';
      },
      legend: ['< -0.4', '-0.4 to 0.0', '0.0 to 0.3', '0.3 to 0.7 (High)', '> 0.7 (Very High)'],
      colors: ['#3b82f6', '#0284c7', '#eab308', '#c2410c', '#7f1d1d']
    }
  };

  const currentConfig = metricConfigs[metric] || metricConfigs.slope;

  // Project GeoJSON coordinates into SVG viewBox bounds (width=400, height=600)
  const { paths, bounds } = useMemo(() => {
    if (!geoJsonData || !geoJsonData.features) return { paths: [], bounds: null };

    // Compute bounding box
    let minLon = 180, maxLon = -180, minLat = 90, maxLat = -90;

    const scanCoords = (coords) => {
      if (typeof coords[0] === 'number') {
        const [lon, lat] = coords;
        if (lon < minLon) minLon = lon;
        if (lon > maxLon) maxLon = lon;
        if (lat < minLat) minLat = lat;
        if (lat > maxLat) maxLat = lat;
      } else {
        coords.forEach(scanCoords);
      }
    };

    geoJsonData.features.forEach((f) => scanCoords(f.geometry.coordinates));

    // Pad slightly
    const lonPadding = (maxLon - minLon) * 0.05;
    const latPadding = (maxLat - minLat) * 0.05;
    minLon -= lonPadding;
    maxLon += lonPadding;
    minLat -= latPadding;
    maxLat += latPadding;

    const width = 360;
    const height = 560;

    const project = ([lon, lat]) => {
      const x = ((lon - minLon) / (maxLon - minLon)) * width + 20;
      // Invert Y for SVG coordinates
      const y = height - ((lat - minLat) / (maxLat - minLat)) * height + 20;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    };

    const convertRing = (ring) => ring.map(project).join(' L ');

    const districtPaths = geoJsonData.features.map((feature) => {
      const name = feature.properties.district;
      let dStr = '';

      if (feature.geometry.type === 'Polygon') {
        dStr = feature.geometry.coordinates
          .map((ring) => `M ${convertRing(ring)} Z`)
          .join(' ');
      } else if (feature.geometry.type === 'MultiPolygon') {
        dStr = feature.geometry.coordinates
          .map((poly) => poly.map((ring) => `M ${convertRing(ring)} Z`).join(' '))
          .join(' ');
      }

      return {
        name,
        d: dStr,
        properties: feature.properties
      };
    });

    return { paths: districtPaths, bounds: { minLon, maxLon, minLat, maxLat } };
  }, [geoJsonData]);

  const activeDistrictInfo = hoveredDistrict 
    ? districtsData?.[hoveredDistrict] 
    : districtsData?.[selectedDistrict];

  const activeDistrictName = hoveredDistrict || selectedDistrict;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-xl backdrop-blur-md flex flex-col justify-between">
      {/* Top Header & Layer Toggles */}
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-semibold text-slate-100">Kerala District Geospatial Explorer</h3>
          </div>
          <span className="text-[11px] text-slate-400">14 Administrative Districts</span>
        </div>

        {/* Metric Layer Buttons */}
        <div className="grid grid-cols-3 sm:grid-cols-6 gap-1.5 mb-3">
          {Object.entries(metricConfigs).map(([key, cfg]) => (
            <button
              key={key}
              onClick={() => setMetric(key)}
              className={`py-1 px-2 text-[11px] font-medium rounded transition ${
                metric === key
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'bg-slate-800/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-transparent'
              }`}
            >
              {cfg.label}
            </button>
          ))}
        </div>
      </div>

      {/* SVG Map Container & Live Info Card */}
      <div className="relative flex flex-col md:flex-row items-center justify-center gap-4 py-2">
        {/* SVG Choropleth Map */}
        <div className="w-full max-w-[340px] aspect-[360/560] relative">
          <svg
            viewBox="0 0 400 600"
            className="w-full h-full drop-shadow-md select-none"
          >
            <defs>
              <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>

            {paths.map(({ name, d }) => {
              const isSelected = selectedDistrict === name;
              const isHovered = hoveredDistrict === name;
              const distData = districtsData?.[name];
              const val = currentConfig.getValue(distData);
              const fillColor = currentConfig.getColor(val);

              return (
                <path
                  key={name}
                  d={d}
                  fill={fillColor}
                  stroke={isSelected ? '#38bdf8' : isHovered ? '#ffffff' : '#0f172a'}
                  strokeWidth={isSelected ? 2.5 : isHovered ? 2 : 1}
                  className="cursor-pointer transition-all duration-150"
                  filter={isSelected ? 'url(#glow)' : undefined}
                  onMouseEnter={() => setHoveredDistrict(name)}
                  onMouseLeave={() => setHoveredDistrict(null)}
                  onClick={() => onSelectDistrict(name)}
                />
              );
            })}
          </svg>
        </div>

        {/* Interactive District Info Panel */}
        <div className="w-full md:w-56 bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-xs flex flex-col gap-2 shadow-lg">
          <div className="flex items-center gap-1.5 pb-2 border-b border-slate-800">
            <MapPin className="w-4 h-4 text-cyan-400" />
            <span className="font-bold text-sm text-slate-100">{activeDistrictName}</span>
          </div>

          {activeDistrictInfo ? (
            <div className="space-y-1.5 text-slate-300">
              <div className="flex justify-between">
                <span className="text-slate-400">Zone:</span>
                <span className="font-medium text-slate-200">{activeDistrictInfo.metadata?.physiographic_zone}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Mean Elevation:</span>
                <span className="font-mono text-slate-200">{activeDistrictInfo.metadata?.mean_elevation_m} m</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Mean Slope:</span>
                <span className="font-mono text-slate-200">{activeDistrictInfo.metadata?.mean_slope_deg}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Norm. Slope (S_norm):</span>
                <span className="font-mono text-cyan-300 font-semibold">{activeDistrictInfo.metadata?.normalized_slope}</span>
              </div>
              <div className="pt-2 border-t border-slate-800 flex justify-between items-baseline">
                <span className="text-slate-400">{currentConfig.label}:</span>
                <span className="font-mono text-sm font-bold text-cyan-400">
                  {currentConfig.getValue(activeDistrictInfo)} {currentConfig.unit}
                </span>
              </div>
            </div>
          ) : (
            <p className="text-slate-500 italic">Hover over map or select district</p>
          )}

          <p className="text-[10px] text-slate-400 italic pt-1">
            Click any district to view its full analytical profile.
          </p>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-2 pt-2 border-t border-slate-800 flex flex-wrap items-center justify-between text-[11px] text-slate-400">
        <span className="font-medium text-slate-300">{currentConfig.label} Scale:</span>
        <div className="flex flex-wrap items-center gap-2">
          {currentConfig.legend.map((leg, idx) => (
            <div key={idx} className="flex items-center gap-1">
              <span
                className="w-2.5 h-2.5 rounded-sm"
                style={{ backgroundColor: currentConfig.colors[idx] }}
              />
              <span className="text-[10px]">{leg}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
