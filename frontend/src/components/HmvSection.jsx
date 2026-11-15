import React, { useState } from 'react';
import { 
  Activity, 
  Flame, 
  Droplets, 
  Trees, 
  Info, 
  ShieldCheck, 
  AlertTriangle,
  Calendar,
  Layers,
  Sliders
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  ComposedChart, 
  Line, 
  Bar, 
  ReferenceLine, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  CartesianGrid 
} from 'recharts';
import StatCard from './StatCard';

export default function HmvSection({ districtData, selectedDistrict, sensitivityData }) {
  const [baselineMode, setBaselineMode] = useState('full'); // 'full' (2015-2024) vs 'early' (2015-2020)
  const timeSeries = districtData?.annual_time_series || [];
  const hmvSeries = timeSeries.filter((d) => d.hmv !== null && d.hmv !== undefined);
  const lastYear = hmvSeries[hmvSeries.length - 1];

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Activity className="w-5 h-5 text-amber-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              HMV — Heat–Moisture–Vegetation Compound Indicator
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            Project-defined formula combining three standardized Earth-system dimensions:
            standardized Land-Surface Temperature (Z_LST), Root-Zone Soil Moisture (Z_SMAP), and Vegetation Index (Z_NDVI).
          </p>
        </div>

        {/* Formula Badge */}
        <div className="bg-slate-950 border border-amber-500/40 rounded-xl px-4 py-2 font-mono text-xs text-amber-300">
          HMV = (Z_LST - Z_SMAP - Z_NDVI) / 3
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="HMV Compound Index (2024)"
          value={lastYear?.hmv ?? '—'}
          unit=""
          subtitle={lastYear?.hmv_condition ?? 'Current state'}
          icon={Activity}
          color="amber"
          trendBadge={
            <span className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded ${
              lastYear?.hmv > 0.5 ? 'bg-rose-950 text-rose-300 border border-rose-800' :
              lastYear?.hmv < -0.5 ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
              'bg-slate-800 text-slate-300 border border-slate-700'
            }`}>
              {lastYear?.hmv_condition}
            </span>
          }
        />

        <StatCard
          title="Thermal Component (Z_LST)"
          value={lastYear?.z_lst !== undefined ? `${lastYear.z_lst > 0 ? '+' : ''}${lastYear.z_lst}` : '—'}
          unit="&sigma;"
          subtitle={`Raw LST: ${lastYear?.lst_celsius} °C`}
          icon={Flame}
          color="rose"
          trendBadge={
            <span className="text-xs text-slate-400">
              Positive adds to thermal stress
            </span>
          }
        />

        <StatCard
          title="Moisture Component (Z_SMAP)"
          value={lastYear?.z_smap !== undefined ? `${lastYear.z_smap > 0 ? '+' : ''}${lastYear.z_smap}` : '—'}
          unit="&sigma;"
          subtitle={`Raw SMAP: ${lastYear?.soil_moisture} m³/m³`}
          icon={Droplets}
          color="cyan"
          trendBadge={
            <span className="text-xs text-slate-400">
              Subtracted in formula (-Z_SMAP)
            </span>
          }
        />

        <StatCard
          title="Vegetation Component (Z_NDVI)"
          value={lastYear?.z_ndvi !== undefined ? `${lastYear.z_ndvi > 0 ? '+' : ''}${lastYear.z_ndvi}` : '—'}
          unit="&sigma;"
          subtitle={`Raw NDVI: ${lastYear?.ndvi}`}
          icon={Trees}
          color="emerald"
          trendBadge={
            <span className="text-xs text-slate-400">
              Subtracted in formula (-Z_NDVI)
            </span>
          }
        />
      </div>

      {/* Main HMV Components Breakdown Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 className="text-base font-bold text-slate-100">
              HMV Index & Standardized Z-Score Components (2015–2024) — {selectedDistrict}
            </h3>
            <p className="text-xs text-slate-400">
              Positive values indicate thermal stress with dry, degraded conditions; negative values indicate cool, moist, lush conditions.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <Sliders className="w-3.5 h-3.5 text-cyan-400 ml-1.5" />
            <span className="text-slate-400">Baseline:</span>
            <button
              onClick={() => setBaselineMode('full')}
              className={`px-2.5 py-1 rounded font-medium transition ${baselineMode === 'full' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              2015–2024 (Full)
            </button>
            <button
              onClick={() => setBaselineMode('early')}
              className={`px-2.5 py-1 rounded font-medium transition ${baselineMode === 'early' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              2015–2020 (Early)
            </button>
          </div>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={hmvSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} label={{ value: 'Standardized Z-Score / HMV', angle: -90, position: 'insideLeft', fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <ReferenceLine y={0} stroke="#475569" strokeWidth={1.5} />
              <ReferenceLine y={0.5} stroke="#f43f5e" strokeDasharray="3 3" label={{ value: '+0.5 Stress Threshold', fill: '#f43f5e', fontSize: 10 }} />
              <ReferenceLine y={-0.5} stroke="#10b981" strokeDasharray="3 3" label={{ value: '-0.5 Moist Threshold', fill: '#10b981', fontSize: 10 }} />

              <Bar dataKey="z_lst" name="Z_LST (Temperature)" fill="#f43f5e" opacity={0.6} />
              <Bar dataKey="z_smap" name="Z_SMAP (Soil Moisture)" fill="#06b6d4" opacity={0.6} />
              <Bar dataKey="z_ndvi" name="Z_NDVI (Vegetation)" fill="#10b981" opacity={0.6} />
              <Line type="monotone" dataKey="hmv" name="HMV Composite" stroke="#f59e0b" strokeWidth={3.5} dot={{ r: 5, fill: '#f59e0b' }} connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Methodology & Sensitivity Summary */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-5 text-xs text-slate-300 space-y-2">
        <h4 className="font-bold text-sm text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
          <Info className="w-4 h-4" />
          HMV Methodological Framework & Physical Meaning
        </h4>
        <p className="leading-relaxed">
          The HMV indicator integrates atmospheric surface heating with hydrological storage and ecological response. 
          When daytime temperatures escalate (positive <span className="font-mono text-rose-300">Z_LST</span>) while root-zone moisture 
          depletes (negative <span className="font-mono text-cyan-300">Z_SMAP</span>) and canopy health degrades 
          (negative <span className="font-mono text-emerald-300">Z_NDVI</span>), the three terms compound to drive HMV above 
          <strong className="text-slate-100">+0.5</strong>, signaling severe environmental drought and heat stress (e.g. during 2016).
        </p>
      </div>
    </div>
  );
}
