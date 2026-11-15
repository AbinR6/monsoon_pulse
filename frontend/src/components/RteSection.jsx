import React from 'react';
import { 
  Mountain, 
  CloudRain, 
  TrendingUp, 
  AlertTriangle, 
  Info, 
  ShieldAlert,
  Layers,
  ArrowRight
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

export default function RteSection({ districtData, selectedDistrict, allDistrictsData }) {
  const timeSeries = districtData?.annual_time_series || [];
  const metadata = districtData?.metadata;
  const lastYear = timeSeries[timeSeries.length - 1];

  // District ranking by 2024 RTE
  const districtRankings = Object.entries(allDistrictsData || {})
    .map(([name, data]) => {
      const ts = data.annual_time_series || [];
      const latest = ts[ts.length - 1];
      return {
        district: name,
        zone: data.metadata?.physiographic_zone,
        mean_slope: data.metadata?.mean_slope_deg,
        s_norm: data.metadata?.normalized_slope,
        r95p_jjas: latest?.r95p_jjas_mm,
        z_r95p: latest?.z_r95p_jjas,
        rte: latest?.rte,
        exposure: latest?.rte_exposure_level
      };
    })
    .sort((a, b) => (b.rte ?? -99) - (a.rte ?? -99));

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Mountain className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              RTE — Rainfall–Terrain Exposure Screening Indicator
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            Combining standardized June–September extreme precipitation (Z_R95p,JJAS) with normalized SRTM terrain slope (S_norm).
            Identifies geographical areas where extreme monsoonal rainfall coincides with high topographic slope exposure.
          </p>
        </div>

        {/* Formula Badge */}
        <div className="bg-slate-950 border border-emerald-500/40 rounded-xl px-4 py-2 font-mono text-xs text-emerald-300">
          RTE = Z_R95p,JJAS &times; S_norm
        </div>
      </div>

      {/* Scientific Screening Disclaimer Alert */}
      <div className="space-y-3">
        <div className="bg-amber-950/40 border border-amber-800/60 rounded-xl p-4 text-xs text-amber-200 flex items-start gap-3">
          <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong>Scientific Scope & Methodology Disclaimer:</strong> The Rainfall-Terrain Exposure (RTE) index is a 
            <strong> geographical screening indicator</strong> designed to quantify where extreme orographic monsoon precipitation 
            coincides with steep slope gradients. It is <em>not</em> a direct measurement of geotechnical landslide probability 
            nor proof of landslide occurrence. Localized slope failures depend on soil lithology, regolith thickness, pore-water pressure, 
            and human land-use alterations.
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-xs text-slate-300 flex items-start gap-3">
          <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong>Mathematical Slope Normalization Boundary Behavior:</strong> When a district possesses the minimum regional slope 
            (such as <strong>Alappuzha</strong>, S_d = 0.82°, S_norm = 0.00), the compound RTE is forced to 0.0 by definition 
            (RTE = Z_R95p &times; 0 = 0). This mathematical boundary indicates <em>near-zero topographical slope hazard</em>, 
            <strong> not an absence of extreme rainfall</strong>. Lowland wetland flooding exposure is tracked independently via 
            raw extreme rainfall (R95p and PRCPTOT).
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="RTE Exposure Index (2024)"
          value={lastYear?.rte ?? '—'}
          unit=""
          subtitle={lastYear?.rte_exposure_level ?? 'Exposure level'}
          icon={Mountain}
          color="emerald"
          trendBadge={
            <span className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded ${
              lastYear?.rte > 0.6 ? 'bg-rose-950 text-rose-300 border border-rose-800' :
              lastYear?.rte > 0.2 ? 'bg-amber-950 text-amber-300 border border-amber-800' :
              'bg-slate-800 text-slate-300 border border-slate-700'
            }`}>
              {lastYear?.rte_exposure_level}
            </span>
          }
        />

        <StatCard
          title="Rainfall Contribution (Z_R95p,JJAS)"
          value={lastYear?.z_r95p_jjas !== undefined ? `${lastYear.z_r95p_jjas > 0 ? '+' : ''}${lastYear.z_r95p_jjas}` : '—'}
          unit="&sigma;"
          subtitle={`Raw JJAS R95p: ${lastYear?.r95p_jjas_mm} mm`}
          icon={CloudRain}
          color="blue"
          trendBadge={
            <span className="text-xs text-slate-400">
              Standardized June–September extreme anomaly
            </span>
          }
        />

        <StatCard
          title="Terrain Contribution (S_norm)"
          value={metadata?.normalized_slope ?? '—'}
          unit=""
          subtitle={`Mean Slope: ${metadata?.mean_slope_deg}° (p90: ${metadata?.p90_slope_deg}°)`}
          icon={Mountain}
          color="amber"
          trendBadge={
            <span className="text-xs text-slate-400">
              Derived from NASA/USGS SRTMGL1 V003
            </span>
          }
        />

        <StatCard
          title="Physiographic Zone"
          value={metadata?.physiographic_zone?.split('/')[0]?.trim() || '—'}
          unit=""
          subtitle={`Mean Elevation: ${metadata?.mean_elevation_m} m`}
          icon={Layers}
          color="violet"
          trendBadge={
            <span className="text-xs text-slate-400">
              Headquarters: {metadata?.headquarters}
            </span>
          }
        />
      </div>

      {/* 2001-2024 Historical RTE Time Series Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div>
          <h3 className="text-base font-bold text-slate-100">
            Historical RTE Progression (2001–2024) — {selectedDistrict}
          </h3>
          <p className="text-xs text-slate-400">
            Displays separate contributions: Standardized JJAS extreme rainfall (Z_R95p,JJAS) scaled by static normalized terrain slope (S_norm = {metadata?.normalized_slope}).
          </p>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={timeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} label={{ value: 'Index Value / Z-Score', angle: -90, position: 'insideLeft', fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <ReferenceLine y={0} stroke="#475569" strokeWidth={1.5} />
              <ReferenceLine y={0.5} stroke="#f59e0b" strokeDasharray="3 3" label={{ value: 'Elevated Exposure (+0.5)', fill: '#f59e0b', fontSize: 10 }} />

              <Bar dataKey="z_r95p_jjas" name="Rainfall Anomaly (Z_R95p,JJAS)" fill="#0ea5e9" opacity={0.65} />
              <Line type="monotone" dataKey="rte" name="RTE Compound Exposure" stroke="#10b981" strokeWidth={3.5} dot={{ r: 4, fill: '#10b981' }} connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* All 14 Districts RTE Comparative Ranking Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-100">
            Kerala 14-District RTE Exposure Screening Matrix (2024)
          </h3>
          <span className="text-xs text-slate-400">Ranked by Compound RTE</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider">
              <tr>
                <th className="py-2.5 px-3">Rank</th>
                <th className="py-2.5 px-3">District</th>
                <th className="py-2.5 px-3">Physiographic Zone</th>
                <th className="py-2.5 px-3">Mean Slope</th>
                <th className="py-2.5 px-3">S_norm</th>
                <th className="py-2.5 px-3">JJAS R95p (mm)</th>
                <th className="py-2.5 px-3">Z_R95p</th>
                <th className="py-2.5 px-3 font-bold text-emerald-300">RTE Value</th>
                <th className="py-2.5 px-3">Exposure Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono">
              {districtRankings.map((row, idx) => {
                const isSelected = row.district === selectedDistrict;
                return (
                  <tr key={row.district} className={isSelected ? 'bg-cyan-950/40 border-l-2 border-cyan-400 font-semibold' : 'hover:bg-slate-800/40'}>
                    <td className="py-2.5 px-3 text-slate-400">#{idx + 1}</td>
                    <td className="py-2.5 px-3 font-sans font-bold text-slate-100">{row.district}</td>
                    <td className="py-2.5 px-3 font-sans text-slate-400">{row.zone}</td>
                    <td className="py-2.5 px-3 text-slate-200">{row.mean_slope}°</td>
                    <td className="py-2.5 px-3 text-cyan-300">{row.s_norm}</td>
                    <td className="py-2.5 px-3 text-slate-200">{row.r95p_jjas} mm</td>
                    <td className="py-2.5 px-3 text-slate-200">{row.z_r95p}</td>
                    <td className="py-2.5 px-3 text-emerald-400 font-bold text-sm">{row.rte}</td>
                    <td className="py-2.5 px-3 font-sans">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        row.exposure?.includes('High') ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                        row.exposure?.includes('Moderate') ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                        'bg-slate-800 text-slate-300 border border-slate-700'
                      }`}>
                        {row.exposure}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
