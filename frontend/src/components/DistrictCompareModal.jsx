import React, { useState } from 'react';
import { X, GitCompare, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import TrendBadge from './TrendBadge';

export default function DistrictCompareModal({ 
  isOpen, 
  onClose, 
  districtsData, 
  districtsList,
  initialDistrictA = 'Wayanad',
  initialDistrictB = 'Palakkad'
}) {
  const [districtA, setDistrictA] = useState(initialDistrictA);
  const [districtB, setDistrictB] = useState(initialDistrictB);

  if (!isOpen) return null;

  const dataA = districtsData?.[districtA];
  const dataB = districtsData?.[districtB];

  const lastYearA = dataA?.annual_time_series?.[dataA.annual_time_series.length - 1];
  const lastYearB = dataB?.annual_time_series?.[dataB.annual_time_series.length - 1];

  const statsA = dataA?.statistics;
  const statsB = dataB?.statistics;

  const compareRows = [
    {
      metric: 'Physiographic Zone',
      valA: dataA?.metadata?.physiographic_zone,
      valB: dataB?.metadata?.physiographic_zone,
      unit: '',
      highlight: false
    },
    {
      metric: 'Mean Elevation',
      valA: `${dataA?.metadata?.mean_elevation_m} m`,
      valB: `${dataB?.metadata?.mean_elevation_m} m`,
      unit: '',
      higherIs: 'higher terrain'
    },
    {
      metric: 'Mean Terrain Slope',
      valA: `${dataA?.metadata?.mean_slope_deg}°`,
      valB: `${dataB?.metadata?.mean_slope_deg}°`,
      unit: '',
      higherIs: 'steeper'
    },
    {
      metric: 'Normalized Slope (S_norm)',
      valA: dataA?.metadata?.normalized_slope,
      valB: dataB?.metadata?.normalized_slope,
      unit: '',
      highlight: true
    },
    {
      metric: 'Total Annual Rainfall (2024)',
      valA: `${lastYearA?.prcptot_annual_mm} mm`,
      valB: `${lastYearB?.prcptot_annual_mm} mm`,
      unit: '',
      highlight: true
    },
    {
      metric: 'JJAS Monsoon Rainfall (2024)',
      valA: `${lastYearA?.prcptot_jjas_mm} mm`,
      valB: `${lastYearB?.prcptot_jjas_mm} mm`,
      unit: '',
      highlight: true
    },
    {
      metric: 'Extreme Rainfall R95p (2024)',
      valA: `${lastYearA?.r95p_annual_mm} mm`,
      valB: `${lastYearB?.r95p_annual_mm} mm`,
      unit: '',
      highlight: true
    },
    {
      metric: 'Mean Land Surface Temp (2024)',
      valA: `${lastYearA?.lst_celsius} °C`,
      valB: `${lastYearB?.lst_celsius} °C`,
      unit: '',
      highlight: true
    },
    {
      metric: 'LST Decadal Trend Rate',
      valA: `+${statsA?.lst_mean?.slope_decadal} °C/dec`,
      valB: `+${statsB?.lst_mean?.slope_decadal} °C/dec`,
      unit: '',
      trendA: statsA?.lst_mean?.trend_direction,
      trendB: statsB?.lst_mean?.trend_direction,
      sigA: statsA?.lst_mean?.significance_class,
      sigB: statsB?.lst_mean?.significance_class
    },
    {
      metric: 'Vegetation NDVI (2024)',
      valA: lastYearA?.ndvi,
      valB: lastYearB?.ndvi,
      unit: '',
      highlight: false
    },
    {
      metric: 'Root-Zone Soil Moisture (2024)',
      valA: `${lastYearA?.soil_moisture} m³/m³`,
      valB: `${lastYearB?.soil_moisture} m³/m³`,
      unit: '',
      highlight: false
    },
    {
      metric: 'HMV Compound Stress (2024)',
      valA: `${lastYearA?.hmv} (${lastYearA?.hmv_condition})`,
      valB: `${lastYearB?.hmv} (${lastYearB?.hmv_condition})`,
      unit: '',
      highlight: true
    },
    {
      metric: 'RTE Exposure Index (2024)',
      valA: `${lastYearA?.rte} (${lastYearA?.rte_exposure_level})`,
      valB: `${lastYearB?.rte} (${lastYearB?.rte_exposure_level})`,
      unit: '',
      highlight: true
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/80">
          <div className="flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-slate-100">District Head-to-Head Comparative Assessment</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* District Selectors */}
        <div className="grid grid-cols-2 gap-4 p-4 bg-slate-950/40 border-b border-slate-800">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">Primary District (A):</label>
            <select
              value={districtA}
              onChange={(e) => setDistrictA(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm font-bold text-cyan-400 focus:outline-none cursor-pointer"
            >
              {districtsList.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">Comparison District (B):</label>
            <select
              value={districtB}
              onChange={(e) => setDistrictB(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm font-bold text-amber-400 focus:outline-none cursor-pointer"
            >
              {districtsList.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Comparative Table */}
        <div className="flex-1 overflow-y-auto p-4">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-950/70 text-slate-400 uppercase tracking-wider sticky top-0">
              <tr>
                <th className="py-2.5 px-3">Environmental Indicator</th>
                <th className="py-2.5 px-3 text-cyan-300 font-mono text-sm">{districtA}</th>
                <th className="py-2.5 px-3 text-amber-300 font-mono text-sm">{districtB}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {compareRows.map((row, idx) => (
                <tr key={idx} className={row.highlight ? 'bg-slate-800/20 hover:bg-slate-800/40' : 'hover:bg-slate-800/30'}>
                  <td className="py-2.5 px-3 font-medium text-slate-300">{row.metric}</td>
                  <td className="py-2.5 px-3 font-mono font-semibold text-slate-100">{row.valA}</td>
                  <td className="py-2.5 px-3 font-mono font-semibold text-slate-100">{row.valB}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-slate-800 bg-slate-950 flex items-center justify-between text-xs text-slate-400">
          <span>Source: NASA GPM, MODIS, SMAP & SRTM analytical outputs.</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-medium transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
