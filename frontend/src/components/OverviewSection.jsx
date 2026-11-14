import React from 'react';
import { 
  CloudRain, 
  Thermometer, 
  Trees, 
  Droplets, 
  Mountain, 
  Activity, 
  ShieldCheck, 
  TrendingUp, 
  AlertTriangle,
  Award,
  Globe2,
  Calendar,
  Layers
} from 'lucide-react';
import StatCard from './StatCard';
import TrendBadge from './TrendBadge';
import InteractiveMap from './InteractiveMap';

export default function OverviewSection({ 
  dashboardData, 
  geoJsonData,
  selectedDistrict, 
  setSelectedDistrict,
  setActiveTab 
}) {
  const districtData = dashboardData?.districts_data?.[selectedDistrict];
  const lastYear = districtData?.annual_time_series?.[districtData.annual_time_series.length - 1];
  const stats = districtData?.statistics;

  return (
    <div className="space-y-6">
      {/* Hero Banner / Mission Brief */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 border border-slate-800 p-6 md:p-8 shadow-2xl">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold uppercase tracking-wider">
            <Globe2 className="w-3.5 h-3.5" />
            NASA Space Apps Challenge 2026 • Earth System Trend Detective
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-mono">
            MONSOON PULSE: Environmental Intelligence for Kerala
          </h2>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
            Investigating long-term multi-variable Earth-system trends across Kerala's 14 administrative districts 
            from <strong className="text-cyan-400">2001 to 2024</strong>. Combining authentic NASA satellite observations 
            to detect what is changing, where it is changing, how rapidly it is shifting, and whether trends 
            are statistically defensible under rigorous false-discovery-rate control.
          </p>

          {/* Quick Discovery Chips */}
          <div className="pt-2 flex flex-wrap gap-2 text-xs">
            <span className="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-slate-300 flex items-center gap-1.5">
              <Thermometer className="w-3.5 h-3.5 text-rose-400" />
              <span>Warming Rate: +0.28°C / decade</span>
            </span>
            <span className="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-slate-300 flex items-center gap-1.5">
              <CloudRain className="w-3.5 h-3.5 text-blue-400" />
              <span>R95p Extreme Rain: Intensifying in Western Ghats</span>
            </span>
            <span className="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-slate-300 flex items-center gap-1.5">
              <Mountain className="w-3.5 h-3.5 text-amber-400" />
              <span>RTE Compound Exposure: Highest in Wayanad & Idukki</span>
            </span>
          </div>
        </div>
      </div>

      {/* KPI Cards Row (Selected District Overview) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Extreme Rain (R95p)"
          value={lastYear?.r95p_annual_mm ?? '—'}
          unit="mm"
          subtitle={`Annual R95p in ${selectedDistrict} (2024)`}
          icon={CloudRain}
          color="blue"
          trendBadge={
            <TrendBadge
              trend={stats?.r95p_annual?.trend_direction}
              pValue={stats?.r95p_annual?.p_value}
              qValue={stats?.r95p_annual?.q_value}
              slope={stats?.r95p_annual?.slope_decadal}
              unit="mm/dec"
            />
          }
        />

        <StatCard
          title="Land Surface Temp"
          value={lastYear?.lst_celsius ?? '—'}
          unit="°C"
          subtitle={`Mean daytime LST (2024)`}
          icon={Thermometer}
          color="rose"
          trendBadge={
            <TrendBadge
              trend={stats?.lst_mean?.trend_direction}
              pValue={stats?.lst_mean?.p_value}
              qValue={stats?.lst_mean?.q_value}
              slope={stats?.lst_mean?.slope_decadal}
              unit="°C/dec"
            />
          }
        />

        <StatCard
          title="HMV Compound Stress"
          value={lastYear?.hmv ?? '—'}
          unit="index"
          subtitle={lastYear?.hmv_condition ?? 'Heat-Moisture-Vegetation'}
          icon={Activity}
          color="amber"
          trendBadge={
            <div className="text-[11px] text-slate-400 flex items-center justify-between">
              <span>Z_LST: {lastYear?.z_lst}</span>
              <span>Z_SMAP: {lastYear?.z_smap}</span>
              <span>Z_NDVI: {lastYear?.z_ndvi}</span>
            </div>
          }
        />

        <StatCard
          title="RTE Exposure Screening"
          value={lastYear?.rte ?? '—'}
          unit="index"
          subtitle={`${lastYear?.rte_exposure_level ?? 'Exposure'} (S_norm: ${districtData?.metadata?.normalized_slope})`}
          icon={Mountain}
          color="emerald"
          trendBadge={
            <div className="text-[11px] text-slate-400 flex items-center justify-between">
              <span>Slope: {districtData?.metadata?.mean_slope_deg}°</span>
              <span>Elev: {districtData?.metadata?.mean_elevation_m}m</span>
            </div>
          }
        />
      </div>

      {/* Main Grid: Interactive Map & 30-Second Mission Investigation Flow */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Kerala District Choropleth Map (7 cols) */}
        <div className="lg:col-span-7">
          <InteractiveMap
            geoJsonData={geoJsonData}
            districtsData={dashboardData?.districts_data}
            selectedDistrict={selectedDistrict}
            onSelectDistrict={setSelectedDistrict}
          />
        </div>

        {/* Right Column: 30-Second Demonstration Script & Key Insights (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {/* Demonstration Guide Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-xl">
            <div className="flex items-center gap-2 mb-3">
              <Award className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
                Judge Demonstration Sequence (30 Seconds)
              </h3>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 flex items-start gap-3">
                <span className="font-mono text-cyan-400 font-bold">0–5s</span>
                <div>
                  <strong className="text-slate-200 block">Mission Introduction</strong>
                  <span className="text-slate-400">MONSOON PULSE investigates Kerala's 14 districts across 2001–2024.</span>
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 flex items-start gap-3">
                <span className="font-mono text-cyan-400 font-bold">5–15s</span>
                <div>
                  <strong className="text-slate-200 block">NASA Multi-Sensor Integration</strong>
                  <span className="text-slate-400">GPM IMERG (Rainfall), MODIS (LST & NDVI), SMAP (Soil Moisture), SRTM (Terrain).</span>
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 flex items-start gap-3">
                <span className="font-mono text-cyan-400 font-bold">15–25s</span>
                <div>
                  <strong className="text-slate-200 block">Compound Indicators & Statistical Rigor</strong>
                  <span className="text-slate-400">Explore HMV thermal stress and RTE slope exposure alongside Mann-Kendall and FDR q-values.</span>
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 flex items-start gap-3">
                <span className="font-mono text-cyan-400 font-bold">25–30s</span>
                <div>
                  <strong className="text-slate-200 block">Verified Scientific Discovery</strong>
                  <span className="text-slate-400">Highland Western Ghats (Wayanad, Idukki) exhibit compounded hydro-topographical risk spikes during extreme monsoon bursts.</span>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Nav Shortcut Buttons */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-xl">
            <h4 className="text-xs uppercase font-semibold text-slate-400 mb-2.5">Deep-Dive Exploration Modules</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                onClick={() => setActiveTab('rainfall')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-left text-slate-200 font-medium transition flex items-center justify-between"
              >
                <span>R95p Rainfall</span>
                <CloudRain className="w-3.5 h-3.5 text-blue-400" />
              </button>
              <button
                onClick={() => setActiveTab('temperature')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-left text-slate-200 font-medium transition flex items-center justify-between"
              >
                <span>Land Temp (LST)</span>
                <Thermometer className="w-3.5 h-3.5 text-rose-400" />
              </button>
              <button
                onClick={() => setActiveTab('hmv')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-left text-slate-200 font-medium transition flex items-center justify-between"
              >
                <span>HMV Indicator</span>
                <Activity className="w-3.5 h-3.5 text-amber-400" />
              </button>
              <button
                onClick={() => setActiveTab('rte')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-left text-slate-200 font-medium transition flex items-center justify-between"
              >
                <span>RTE Screening</span>
                <Mountain className="w-3.5 h-3.5 text-emerald-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
