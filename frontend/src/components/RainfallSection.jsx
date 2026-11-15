import React from 'react';
import { 
  CloudRain, 
  Droplets, 
  TrendingUp, 
  Calendar, 
  Info, 
  AlertTriangle,
  Layers,
  Sparkles
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  ComposedChart, 
  Bar, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  CartesianGrid 
} from 'recharts';
import StatCard from './StatCard';
import TrendBadge from './TrendBadge';

export default function RainfallSection({ districtData, selectedDistrict }) {
  const timeSeries = districtData?.annual_time_series || [];
  const stats = districtData?.statistics || {};
  const lastYear = timeSeries[timeSeries.length - 1];

  const statR95p = stats?.r95p_annual;
  const statJjas = stats?.prcptot_jjas;
  const thresholdP95 = statR95p?.threshold_p95_mm ?? lastYear?.threshold_p95_mm ?? timeSeries.find((d) => d.threshold_p95_mm)?.threshold_p95_mm;

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <CloudRain className="w-5 h-5 text-blue-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              Extreme Precipitation & ETCCDI R95p Analysis
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            NASA GPM IMERG V07 (0.1°, half-hourly integrated to daily accumulation, 2001–2024).
            Evaluating conventional annual R95p and seasonal South-West monsoon (June–September) extremes.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <Calendar className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-300">Baseline Reference: <strong className="text-cyan-300">2001–2020</strong></span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="R95p Extreme Rain (2024)"
          value={lastYear?.r95p_annual_mm ?? '—'}
          unit="mm"
          subtitle={`Precipitation on days > P95 threshold (${thresholdP95 ? thresholdP95 + ' mm/day' : '—'})`}
          icon={CloudRain}
          color="blue"
          trendBadge={
            <TrendBadge
              trend={statR95p?.trend_direction}
              pValue={statR95p?.p_value}
              qValue={statR95p?.q_value}
              slope={statR95p?.slope_decadal}
              unit="mm/dec"
            />
          }
        />

        <StatCard
          title="JJAS Monsoon Rain (2024)"
          value={lastYear?.prcptot_jjas_mm ?? '—'}
          unit="mm"
          subtitle={`June–September accumulated rain`}
          icon={Droplets}
          color="cyan"
          trendBadge={
            <TrendBadge
              trend={statJjas?.trend_direction}
              pValue={statJjas?.p_value}
              qValue={statJjas?.q_value}
              slope={statJjas?.slope_decadal}
              unit="mm/dec"
            />
          }
        />

        <StatCard
          title="R95pTOT Fraction of Total"
          value={lastYear?.r95p_fraction_pct ?? '—'}
          unit="%"
          subtitle={`ETCCDI R95pTOT: proportion of annual rain from extremes`}
          icon={Sparkles}
          color="amber"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Total Rain: {lastYear?.prcptot_annual_mm ?? '—'} mm
            </span>
          }
        />

        <StatCard
          title="Max 1-Day Rain (RX1day)"
          value={lastYear?.rx1day_mm ?? '—'}
          unit="mm"
          subtitle={`Single day precipitation peak`}
          icon={AlertTriangle}
          color="rose"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Extreme Days (P &gt; P95): {lastYear?.extreme_days_count ?? '—'} days
            </span>
          }
        />
      </div>

      {/* Primary Chart: Annual Total vs JJAS vs R95p */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-100">
              Annual Precipitation & Extreme R95p Progression ({selectedDistrict})
            </h3>
            <p className="text-xs text-slate-400">
              Notice the extreme rainfall spikes during the 2018 Great Flood, 2019 landslides, and 2024 bursts.
            </p>
          </div>
          <span className="text-xs font-mono text-cyan-400 bg-cyan-950 px-2.5 py-1 rounded border border-cyan-800">
            District P95 Baseline: <strong className="text-cyan-200">{thresholdP95 ? `${thresholdP95} mm/day` : '—'}</strong>
          </span>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis yAxisId="left" stroke="#38bdf8" tick={{ fontSize: 11 }} label={{ value: 'Precipitation (mm)', angle: -90, position: 'insideLeft', fill: '#38bdf8', fontSize: 11 }} />
              <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" tick={{ fontSize: 11 }} label={{ value: 'R95p Fraction (%)', angle: 90, position: 'insideRight', fill: '#f59e0b', fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Bar yAxisId="left" dataKey="prcptot_annual_mm" name="Annual Total Rain (mm)" fill="#0284c7" opacity={0.65} />
              <Bar yAxisId="left" dataKey="prcptot_jjas_mm" name="JJAS Monsoon Rain (mm)" fill="#0ea5e9" opacity={0.85} />
              <Line yAxisId="left" type="monotone" dataKey="r95p_annual_mm" name="R95p Annual (mm)" stroke="#f43f5e" strokeWidth={3} dot={{ r: 3 }} connectNulls={false} />
              <Line yAxisId="left" type="monotone" dataKey="r95p_jjas_mm" name="R95p JJAS Monsoon (mm)" stroke="#a855f7" strokeWidth={2} strokeDasharray="4 4" dot={{ r: 2 }} connectNulls={false} />
              <Line yAxisId="right" type="monotone" dataKey="r95p_fraction_pct" name="R95pTOT Fraction (%)" stroke="#f59e0b" strokeWidth={2} dot={false} connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Scientific ETCCDI Definition Callout */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-5 text-xs text-slate-300 space-y-2">
        <h4 className="font-bold text-sm text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
          <Info className="w-4 h-4" />
          ETCCDI Scientific R95p & R95pTOT Methodology
        </h4>
        <p className="leading-relaxed">
          The Expert Team on Climate Change Detection and Indices (ETCCDI) defines <strong>R95p</strong> as the annual accumulated 
          precipitation on wet days (daily rainfall <span className="font-mono text-cyan-300">&ge; 1.0 mm</span>) that exceeds 
          the district-specific 95th percentile (P95) calculated from baseline wet days (<strong className="text-slate-100">2001–2020</strong>).
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 font-mono text-[11px] text-slate-300">
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <strong>Annual R95p (mm):</strong>
            <div className="text-cyan-300 mt-1">R95p = &sum; [ P_d | P_d &gt; P_95 ]</div>
            <div className="text-[10px] text-slate-400 mt-1">Total depth from very wet days</div>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <strong>JJAS Monsoon R95p (mm):</strong>
            <div className="text-cyan-300 mt-1">R95p_JJAS = &sum; [ P_d,JJAS | P_d &gt; P_95 ]</div>
            <div className="text-[10px] text-slate-400 mt-1">SW-monsoon extreme depth</div>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <strong>R95pTOT Fraction (%):</strong>
            <div className="text-amber-300 mt-1">R95pTOT = (R95p / PRCPTOT) &times; 100%</div>
            <div className="text-[10px] text-slate-400 mt-1">Extreme contribution fraction</div>
          </div>
        </div>
      </div>
    </div>
  );
}
