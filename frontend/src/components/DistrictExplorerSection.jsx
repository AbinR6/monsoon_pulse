import React, { useState } from 'react';
import { 
  MapPin, 
  Mountain, 
  Compass, 
  Layers, 
  CloudRain, 
  Thermometer, 
  Trees, 
  Droplets, 
  Activity,
  TrendingUp,
  ShieldAlert
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  ComposedChart, 
  Line, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  CartesianGrid 
} from 'recharts';
import StatCard from './StatCard';
import TrendBadge from './TrendBadge';

export default function DistrictExplorerSection({ 
  districtData, 
  selectedDistrict, 
  setSelectedDistrict, 
  districtsList 
}) {
  const [activeMetric, setActiveMetric] = useState('rainfall');
  const metadata = districtData?.metadata;
  const timeSeries = districtData?.annual_time_series || [];
  const stats = districtData?.statistics || {};
  const lastYear = timeSeries[timeSeries.length - 1];

  return (
    <div className="space-y-6">
      {/* District Header Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400">
              <MapPin className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-bold font-mono text-white">{selectedDistrict}</h2>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-800 text-cyan-300 border border-slate-700">
                  {metadata?.physiographic_zone}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Headquarters: <strong className="text-slate-300">{metadata?.headquarters || selectedDistrict}</strong> • Area: <strong className="text-slate-300">{metadata?.area_sq_km?.toLocaleString()} km²</strong>
              </p>
            </div>
          </div>

          {/* District Switcher Quick Pills */}
          <div className="flex flex-wrap items-center gap-1.5 max-w-lg">
            {districtsList.map((d) => (
              <button
                key={d}
                onClick={() => setSelectedDistrict(d)}
                className={`px-2.5 py-1 text-xs rounded-lg transition font-medium ${
                  selectedDistrict === d
                    ? 'bg-cyan-500 text-slate-950 font-bold shadow'
                    : 'bg-slate-800/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Physiographic Profile Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-xs">
          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <span className="text-slate-400 block">Mean Elevation</span>
            <span className="text-lg font-mono font-bold text-slate-100">{metadata?.mean_elevation_m} m</span>
            <span className="text-[10px] text-slate-400 block">p90: {metadata?.p90_elevation_m} m</span>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <span className="text-slate-400 block">Mean Terrain Slope</span>
            <span className="text-lg font-mono font-bold text-slate-100">{metadata?.mean_slope_deg}°</span>
            <span className="text-[10px] text-slate-400 block">p90: {metadata?.p90_slope_deg}°</span>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <span className="text-slate-400 block">Normalized Slope (S_norm)</span>
            <span className="text-lg font-mono font-bold text-cyan-400">{metadata?.normalized_slope}</span>
            <span className="text-[10px] text-slate-400 block">Scale: [0, 1]</span>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <span className="text-slate-400 block">Environmental Trajectory</span>
            <span className="text-sm font-semibold text-amber-300 block mt-1">
              {stats?.lst_mean?.slope_decadal > 0.25 ? 'High Warming' : 'Moderate Warming'}
            </span>
            <span className="text-[10px] text-slate-400 block">R95p: {stats?.r95p_annual?.trend_direction}</span>
          </div>
        </div>

        {metadata?.characteristics && (
          <p className="text-xs text-slate-400 mt-3 italic border-t border-slate-800/80 pt-2">
            "{metadata.characteristics}"
          </p>
        )}
      </div>

      {/* 24-Year Multi-Variable Historical Time Series Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 className="text-base font-bold text-slate-100">Historical Observation Trajectory (2001–2024)</h3>
            <p className="text-xs text-slate-400">Integrated multi-variable trajectory for {selectedDistrict}</p>
          </div>

          {/* Metric Selector Tabs */}
          <div className="flex flex-wrap gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <button
              onClick={() => setActiveMetric('rainfall')}
              className={`px-3 py-1 rounded font-medium transition ${activeMetric === 'rainfall' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              Rainfall & R95p
            </button>
            <button
              onClick={() => setActiveMetric('temperature')}
              className={`px-3 py-1 rounded font-medium transition ${activeMetric === 'temperature' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              LST Temperature
            </button>
            <button
              onClick={() => setActiveMetric('indices')}
              className={`px-3 py-1 rounded font-medium transition ${activeMetric === 'indices' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              HMV & RTE Indices
            </button>
          </div>
        </div>

        {/* Chart View */}
        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            {activeMetric === 'rainfall' ? (
              <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis yAxisId="left" stroke="#38bdf8" tick={{ fontSize: 11 }} label={{ value: 'Annual Rain (mm)', angle: -90, position: 'insideLeft', fill: '#38bdf8', fontSize: 11 }} />
                <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" tick={{ fontSize: 11 }} label={{ value: 'R95p Extreme (mm)', angle: 90, position: 'insideRight', fill: '#f59e0b', fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Bar yAxisId="left" dataKey="prcptot_annual_mm" name="Total Rainfall (mm)" fill="#0284c7" opacity={0.7} />
                <Bar yAxisId="left" dataKey="prcptot_jjas_mm" name="JJAS Monsoon Rain (mm)" fill="#0ea5e9" opacity={0.8} />
                <Line yAxisId="right" type="monotone" dataKey="r95p_annual_mm" name="R95p Extreme (mm)" stroke="#f59e0b" strokeWidth={2.5} dot={{ r: 3 }} />
              </ComposedChart>
            ) : activeMetric === 'temperature' ? (
              <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#f43f5e" tick={{ fontSize: 11 }} domain={['auto', 'auto']} label={{ value: 'Mean LST (°C)', angle: -90, position: 'insideLeft', fill: '#f43f5e', fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="lst_celsius" name="Daytime LST (°C)" stroke="#f43f5e" strokeWidth={3} dot={{ r: 4 }} />
              </ComposedChart>
            ) : (
              <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis yAxisId="left" stroke="#eab308" tick={{ fontSize: 11 }} label={{ value: 'HMV Index', angle: -90, position: 'insideLeft', fill: '#eab308', fontSize: 11 }} />
                <YAxis yAxisId="right" orientation="right" stroke="#10b981" tick={{ fontSize: 11 }} label={{ value: 'RTE Index', angle: 90, position: 'insideRight', fill: '#10b981', fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Line yAxisId="left" type="monotone" dataKey="hmv" name="HMV (Heat-Moisture-Veg)" stroke="#eab308" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line yAxisId="right" type="monotone" dataKey="rte" name="RTE (Rainfall-Terrain)" stroke="#10b981" strokeWidth={2.5} dot={{ r: 3 }} />
              </ComposedChart>
            )}
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
