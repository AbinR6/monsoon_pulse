import React from 'react';
import { 
  Trees, 
  Leaf, 
  TrendingUp, 
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

export default function VegetationSection({ districtData, selectedDistrict }) {
  const timeSeries = districtData?.annual_time_series || [];
  const stats = districtData?.statistics?.ndvi_mean;
  const lastYear = timeSeries[timeSeries.length - 1];

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Trees className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              Vegetation Indices (NDVI) & Canopy Resilience
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            MODIS Terra MOD13Q1 V6.1 (250 m spatial resolution, 16-day composites, 2001–2024).
            Filtered via SummaryQA (&le; 1), scale factor 0.0001.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <Leaf className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-300">Scale: <strong className="text-cyan-300">-0.2 to +1.0</strong></span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Mean NDVI (2024)"
          value={lastYear?.ndvi ?? '—'}
          unit=""
          subtitle={`Annual average canopy greenness`}
          icon={Leaf}
          color="emerald"
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
          title="Decadal Trend Rate"
          value={stats?.slope_decadal !== undefined ? `${stats?.slope_decadal > 0 ? '+' : ''}${stats?.slope_decadal}` : '—'}
          unit="units / decade"
          subtitle={`Theil-Sen slope estimate`}
          icon={TrendingUp}
          color="cyan"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              95% CI: [{stats?.ci_lower * 10}, {stats?.ci_upper * 10}]
            </span>
          }
        />

        <StatCard
          title="24-Year Mean Baseline"
          value={stats?.mean_value ?? '—'}
          unit=""
          subtitle={`Long-term climatological mean`}
          icon={Trees}
          color="amber"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              Total Change: {stats?.pct_change}%
            </span>
          }
        />

        <StatCard
          title="Statistical Significance"
          value={stats?.significance_class?.includes('Significant') ? 'Significant' : 'Stable'}
          unit=""
          subtitle={`FDR-adjusted (q = ${stats?.q_value})`}
          icon={ShieldCheck}
          color="violet"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              p: {stats?.p_value} • &tau;: {stats?.kendalls_tau}
            </span>
          }
        />
      </div>

      {/* NDVI Time Series Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-100">
              Historical Vegetation Greenness NDVI ({selectedDistrict})
            </h3>
            <p className="text-xs text-slate-400">
              Notice the vegetative resilience and the distinct greenness reduction during the 2016 drought.
            </p>
          </div>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#10b981" tick={{ fontSize: 11 }} domain={['dataMin - 0.05', 'dataMax + 0.05']} label={{ value: 'NDVI', angle: -90, position: 'insideLeft', fill: '#10b981', fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Area type="monotone" dataKey="ndvi" name="NDVI Canopy Greenness" stroke="#10b981" fill="#10b981" fillOpacity={0.15} />
              <Line type="monotone" dataKey="ndvi" name="Annual Mean NDVI" stroke="#34d399" strokeWidth={3} dot={{ r: 4 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Scientific Insights */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-5 text-xs text-slate-300 space-y-2">
        <h4 className="font-bold text-sm text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
          <Info className="w-4 h-4" />
          Vegetation Phenology & Forest Canopy Gradients
        </h4>
        <p className="leading-relaxed">
          Kerala's Western Ghats districts (<strong>Idukki</strong>, <strong>Wayanad</strong>, and <strong>Pathanamthitta</strong>) 
          exhibit consistently high NDVI (<strong className="text-slate-100">0.75–0.88</strong>), reflecting dense tropical moist 
          deciduous and evergreen shola forest biomes. Coastal and urban districts (<strong>Ernakulam</strong>, <strong>Alappuzha</strong>) 
          show lower mean NDVI (<strong className="text-slate-100">0.48–0.60</strong>) due to built environments and coastal wetlands.
        </p>
      </div>
    </div>
  );
}
