import React from 'react';
import { 
  Droplets, 
  TrendingUp, 
  AlertTriangle, 
  Info, 
  ShieldCheck,
  Calendar,
  Layers
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  ComposedChart, 
  Line, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  CartesianGrid 
} from 'recharts';
import StatCard from './StatCard';
import TrendBadge from './TrendBadge';

export default function SoilMoistureSection({ districtData, selectedDistrict }) {
  const timeSeries = districtData?.annual_time_series || [];
  // Filter to SMAP available years (2015-2024)
  const smapSeries = timeSeries.filter((d) => d.soil_moisture !== null && d.soil_moisture !== undefined);
  const stats = districtData?.statistics?.sm_mean;
  const lastYear = smapSeries[smapSeries.length - 1];

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Droplets className="w-5 h-5 text-teal-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              Root-Zone Soil Moisture (NASA SMAP L4)
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            NASA SMAP SPL4SMGP V008 (9 km EASE-Grid 2.0, 0–100 cm root-zone depth, 2015–2024).
            Sub-surface hydrological water content and saturation precursor dynamics.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <Calendar className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-300">Observation Window: <strong className="text-cyan-300">2015–2024 (10 Yrs)</strong></span>
        </div>
      </div>

      {/* Sorter Window Explanation Alert */}
      <div className="bg-cyan-950/40 border border-cyan-800/60 rounded-xl p-4 text-xs text-cyan-200 flex items-start gap-3">
        <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>Mission Timing Note:</strong> NASA's Soil Moisture Active Passive (SMAP) observatory launched in January 2015. 
          Its science data products begin in April 2015. Consequently, soil-moisture analyses and the 3-variable HMV composite 
          are rigorously evaluated over the <strong>2015–2024 common multi-sensor window</strong>, avoiding invalid historical backcasting.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Root-Zone Moisture (2024)"
          value={lastYear?.soil_moisture ?? '—'}
          unit="m³ / m³"
          subtitle={`Volumetric fraction (0–100 cm depth)`}
          icon={Droplets}
          color="cyan"
          trendBadge={
            <TrendBadge
              trend={stats?.trend_direction}
              pValue={stats?.p_value}
              qValue={stats?.q_value}
              slope={stats?.slope_decadal}
              unit="/dec"
            />
          }
        />

        <StatCard
          title="10-Year Mean Baseline"
          value={stats?.mean_value ?? '—'}
          unit="m³ / m³"
          subtitle={`Climatological soil water baseline`}
          icon={Droplets}
          color="emerald"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Theil-Sen Slope: {stats?.slope} / yr
            </span>
          }
        />

        <StatCard
          title="Peak Monsoon Saturation"
          value="~0.42–0.48"
          unit="m³ / m³"
          subtitle={`Near field capacity in Ghats`}
          icon={AlertTriangle}
          color="amber"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Pre-monsoon dip: ~0.15–0.20
            </span>
          }
        />

        <StatCard
          title="Statistical Significance"
          value={
            stats?.q_value !== undefined && stats?.q_value < 0.05
              ? 'FDR Significant'
              : stats?.p_value !== undefined && stats?.p_value < 0.05
              ? 'Marginal (Unadj Sig)'
              : 'Not Significant'
          }
          unit=""
          subtitle={`FDR-adjusted (q = ${stats?.q_value ?? '—'})`}
          icon={ShieldCheck}
          color="violet"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              p: {stats?.p_value ?? '—'} • Z: {stats?.z_statistic ?? '—'}
            </span>
          }
        />
      </div>

      {/* Soil Moisture Chart (2015-2024) */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-100">
              SMAP Root-Zone Soil Moisture Time Series (2015–2024) — {selectedDistrict}
            </h3>
            <p className="text-xs text-slate-400">
              Satellite observation of sub-surface volumetric water content (0–100 cm depth). Note saturation peaks during high-monsoon years.
            </p>
          </div>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={smapSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis 
                stroke="#06b6d4" 
                tick={{ fontSize: 11 }} 
                domain={[0.15, 0.45]} 
                tickFormatter={(val) => Number(val).toFixed(3)}
                label={{ value: 'Soil Moisture (m³/m³)', angle: -90, position: 'insideLeft', fill: '#06b6d4', fontSize: 11 }} 
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} 
                formatter={(val) => [Number(val).toFixed(4) + ' m³/m³', 'Soil Moisture']}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Area type="monotone" dataKey="soil_moisture" name="Root-Zone Moisture (m³/m³)" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.2} connectNulls={false} />
              <Line type="monotone" dataKey="soil_moisture" name="Annual Mean Moisture" stroke="#22d3ee" strokeWidth={3} dot={{ r: 5 }} connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
