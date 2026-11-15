import React from 'react';
import { 
  Thermometer, 
  TrendingUp, 
  Sun, 
  Info, 
  Flame, 
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

export default function TemperatureSection({ districtData, selectedDistrict }) {
  const timeSeries = districtData?.annual_time_series || [];
  const stats = districtData?.statistics?.lst_mean;
  const lastYear = timeSeries[timeSeries.length - 1];

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Thermometer className="w-5 h-5 text-rose-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              Land Surface Temperature (LST) & Thermal Trajectory
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            MODIS Terra MOD11A2 V6.1 (1 km spatial resolution, 8-day daytime composites, 2001–2024).
            Filtered using mandatory QC bitmask flags (QC_Day bits 0–1 &le; 01).
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <Sun className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-300">Observation Window: <strong className="text-cyan-300">2001–2024 (24 Yrs)</strong></span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Mean Daytime LST (2024)"
          value={lastYear?.lst_celsius ?? '—'}
          unit="°C"
          subtitle={`Annual daytime average in ${selectedDistrict}`}
          icon={Thermometer}
          color="rose"
          trendBadge={
            <TrendBadge
              trend={stats?.trend_direction}
              pValue={stats?.p_value}
              qValue={stats?.q_value}
              slope={stats?.slope_decadal}
              unit="°C/dec"
            />
          }
        />

        <StatCard
          title="Decadal Warming Rate"
          value={stats?.slope_decadal !== undefined ? `+${stats?.slope_decadal}` : '—'}
          unit="°C / decade"
          subtitle={`Theil-Sen robust estimator`}
          icon={TrendingUp}
          color="amber"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              95% CI: [{stats?.ci_lower * 10}, {stats?.ci_upper * 10}]
            </span>
          }
        />

        <StatCard
          title="Overall 24-Year Change"
          value={stats?.pct_change !== undefined ? `+${stats?.pct_change}` : '—'}
          unit="%"
          subtitle={`Total percentage change over window`}
          icon={Flame}
          color="violet"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Mean: {stats?.mean_value} °C
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
          color={stats?.q_value < 0.05 ? "emerald" : "amber"}
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Kendall's &tau;: {stats?.kendalls_tau ?? '—'} • Z: {stats?.z_statistic ?? '—'}
            </span>
          }
        />
      </div>

      {/* LST Time Series Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-100">
              Historical Daytime Land Surface Temperature ({selectedDistrict})
            </h3>
            <p className="text-xs text-slate-400">
              MODIS MOD11A2 1km daytime thermal observations (2001–2024). Note elevation-dependent baseline cooling in the Ghats and regional drought peaks.
            </p>
          </div>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis 
                stroke="#f43f5e" 
                tick={{ fontSize: 11 }} 
                domain={['dataMin - 1', 'dataMax + 1']} 
                tickFormatter={(val) => Number(val).toFixed(1)}
                label={{ value: 'Daytime LST (°C)', angle: -90, position: 'insideLeft', fill: '#f43f5e', fontSize: 11 }} 
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} 
                formatter={(val) => [Number(val).toFixed(2) + ' °C', 'Daytime LST']}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Area type="monotone" dataKey="lst_celsius" name="Daytime LST (°C)" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.15} connectNulls={false} />
              <Line type="monotone" dataKey="lst_celsius" name="LST Trend Line" stroke="#fb7185" strokeWidth={3} dot={{ r: 4 }} connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Scientific Insights */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-5 text-xs text-slate-300 space-y-2">
        <h4 className="font-bold text-sm text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
          <Info className="w-4 h-4" />
          Physiographic Temperature Dynamics in Kerala
        </h4>
        <p className="leading-relaxed">
          Kerala exhibits striking physiographic thermal differentiation. The <strong>Palakkad Gap</strong> functions 
          as a thermal hotspot where inland continental dry heat channels through the mountain break, producing summer LST 
          exceeding <strong className="text-slate-100">36–38°C</strong>. In contrast, the highland districts of <strong>Idukki</strong> 
          and <strong>Wayanad</strong> maintain temperate LST (<strong className="text-slate-100">22–27°C</strong>) due to elevation 
          lapse rates and dense forest canopy evapotranspiration.
        </p>
      </div>
    </div>
  );
}
