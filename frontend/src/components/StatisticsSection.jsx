import React, { useState, useMemo } from 'react';
import { 
  BarChart3, 
  ShieldCheck, 
  AlertTriangle, 
  Filter, 
  Search, 
  Sliders, 
  Info,
  CheckCircle2,
  XCircle,
  HelpCircle
} from 'lucide-react';
import StatCard from './StatCard';

export default function StatisticsSection({ dashboardData, selectedDistrict, setSelectedDistrict }) {
  const [districtFilter, setDistrictFilter] = useState('ALL');
  const [variableFilter, setVariableFilter] = useState('ALL');
  const [significanceFilter, setSignificanceFilter] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');

  const allTests = dashboardData?.all_statistical_tests || [];
  const sensitivityScenarios = dashboardData?.sensitivity_analysis || [];

  // Summary counts
  const totalTests = allTests.length;
  const fdrSignificant = allTests.filter((t) => t.significance_class?.includes('FDR-Controlled')).length;
  const unadjSignificant = allTests.filter((t) => t.significance_class?.includes('Unadjusted Only')).length;
  const insignificant = allTests.filter((t) => t.significance_class?.includes('Insignificant')).length;

  // Filtered rows
  const filteredTests = useMemo(() => {
    return allTests.filter((item) => {
      if (districtFilter !== 'ALL' && item.district !== districtFilter) return false;
      if (variableFilter !== 'ALL' && item.variable_key !== variableFilter) return false;
      if (significanceFilter !== 'ALL' && !item.significance_class?.includes(significanceFilter)) return false;
      if (searchTerm) {
        const query = searchTerm.toLowerCase();
        return (
          item.district.toLowerCase().includes(query) ||
          item.variable_title.toLowerCase().includes(query) ||
          item.trend_direction.toLowerCase().includes(query)
        );
      }
      return true;
    });
  }, [allTests, districtFilter, variableFilter, significanceFilter, searchTerm]);

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <BarChart3 className="w-5 h-5 text-cyan-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              Rigorous Statistical Evaluation & Multi-Testing Control
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            Mann–Kendall non-parametric monotonic trend testing, Theil–Sen median slope estimation with 95% rank-based confidence intervals, 
            lag-1 serial autocorrelation assessment, and Benjamini–Hochberg False Discovery Rate (FDR) multi-testing adjustment.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-300">Total Hypotheses Evaluated: <strong className="text-cyan-300">70 Simultaneous Tests</strong></span>
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Trend Hypotheses"
          value={totalTests}
          unit="tests"
          subtitle="14 districts &times; 5 environmental variables"
          icon={BarChart3}
          color="cyan"
        />

        <StatCard
          title="FDR-Controlled Significant"
          value={fdrSignificant}
          unit="tests"
          subtitle="Survives Benjamini-Hochberg &alpha;=0.05"
          icon={CheckCircle2}
          color="emerald"
          trendBadge={
            <span className="text-xs text-emerald-400 font-mono font-semibold">
              {((fdrSignificant / totalTests) * 100).toFixed(1)}% of hypotheses
            </span>
          }
        />

        <StatCard
          title="Marginally Significant"
          value={unadjSignificant}
          unit="tests"
          subtitle="p < 0.05 but rejected under FDR (q &ge; 0.05)"
          icon={AlertTriangle}
          color="amber"
          trendBadge={
            <span className="text-xs text-amber-400 font-mono">
              Potential false discoveries
            </span>
          }
        />

        <StatCard
          title="Statistically Insignificant"
          value={insignificant}
          unit="tests"
          subtitle="No monotonic trend detected (p &ge; 0.05)"
          icon={XCircle}
          color="slate"
          trendBadge={
            <span className="text-xs text-slate-400 font-mono">
              {((insignificant / totalTests) * 100).toFixed(1)}% of hypotheses
            </span>
          }
        />
      </div>

      {/* Controls & Filters Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-3">
          {/* Search Input */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
            <input
              type="text"
              placeholder="Filter district or variable..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-48 sm:w-56"
            />
          </div>

          {/* District Filter */}
          <select
            value={districtFilter}
            onChange={(e) => setDistrictFilter(e.target.value)}
            className="bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none"
          >
            <option value="ALL">All Districts (14)</option>
            {Object.keys(dashboardData?.districts_data || {}).map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>

          {/* Variable Filter */}
          <select
            value={variableFilter}
            onChange={(e) => setVariableFilter(e.target.value)}
            className="bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none"
          >
            <option value="ALL">All Variables (5)</option>
            <option value="r95p_annual">Extreme Rain R95p</option>
            <option value="prcptot_jjas">Monsoon Rain (JJAS)</option>
            <option value="lst_mean">Land Surface Temp (LST)</option>
            <option value="ndvi_mean">Vegetation (NDVI)</option>
            <option value="sm_mean">Soil Moisture (SMAP)</option>
          </select>

          {/* Significance Filter */}
          <select
            value={significanceFilter}
            onChange={(e) => setSignificanceFilter(e.target.value)}
            className="bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none"
          >
            <option value="ALL">All Results</option>
            <option value="FDR-Controlled">FDR Significant Only</option>
            <option value="Unadjusted Only">Marginal Only</option>
            <option value="Insignificant">Insignificant Only</option>
          </select>
        </div>

        <span className="text-slate-400 font-mono">
          Showing <strong>{filteredTests.length}</strong> of {totalTests} tests
        </span>
      </div>

      {/* Complete Statistical Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
        <h3 className="text-base font-bold text-slate-100">
          The 70-Test Multi-Testing Analytical Matrix
        </h3>

        <div className="overflow-x-auto max-h-[500px] overflow-y-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider sticky top-0 z-10 shadow-sm">
              <tr>
                <th className="py-2.5 px-3">District</th>
                <th className="py-2.5 px-3">Variable</th>
                <th className="py-2.5 px-3">Obs (n)</th>
                <th className="py-2.5 px-3">Window</th>
                <th className="py-2.5 px-3">Direction</th>
                <th className="py-2.5 px-3">Theil-Sen Slope</th>
                <th className="py-2.5 px-3">95% CI</th>
                <th className="py-2.5 px-3">Kendall's &tau;</th>
                <th className="py-2.5 px-3">Z-Score</th>
                <th className="py-2.5 px-3">Raw p-value</th>
                <th className="py-2.5 px-3">BH q-value</th>
                <th className="py-2.5 px-3">Lag-1 r1</th>
                <th className="py-2.5 px-3">Significance Class</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono">
              {filteredTests.map((row, idx) => {
                const isFdr = row.significance_class?.includes('FDR-Controlled');
                const isMarginal = row.significance_class?.includes('Unadjusted Only');
                return (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-2.5 px-3 font-sans font-bold text-slate-200">{row.district}</td>
                    <td className="py-2.5 px-3 font-sans text-slate-300">{row.variable_title}</td>
                    <td className="py-2.5 px-3 text-slate-400">{row.n_observations}</td>
                    <td className="py-2.5 px-3 text-slate-400">{row.observation_period}</td>
                    <td className="py-2.5 px-3 font-sans">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        row.trend_direction === 'Increasing' ? 'bg-rose-950/80 text-rose-300' :
                        row.trend_direction === 'Decreasing' ? 'bg-emerald-950/80 text-emerald-300' :
                        'bg-slate-800 text-slate-400'
                      }`}>
                        {row.trend_direction}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-100 font-bold">
                      {row.slope > 0 ? `+${row.slope}` : row.slope} {row.unit}
                    </td>
                    <td className="py-2.5 px-3 text-slate-400 text-[11px]">
                      [{row.ci_lower}, {row.ci_upper}]
                    </td>
                    <td className="py-2.5 px-3 text-slate-300">{row.kendalls_tau}</td>
                    <td className="py-2.5 px-3 text-slate-300">{row.z_statistic}</td>
                    <td className="py-2.5 px-3 text-slate-200 font-bold">{row.p_value}</td>
                    <td className="py-2.5 px-3 text-cyan-300 font-bold">{row.q_value}</td>
                    <td className="py-2.5 px-3 text-slate-400">{row.lag1_autocorr}</td>
                    <td className="py-2.5 px-3 font-sans">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        isFdr ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                        isMarginal ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                        'bg-slate-800 text-slate-400 border border-slate-700'
                      }`}>
                        {row.significance_class}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Sensitivity Analysis Scenarios */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center gap-2">
          <Sliders className="w-5 h-5 text-amber-400" />
          <h3 className="text-base font-bold text-slate-100">
            Methodological Sensitivity Analysis
          </h3>
        </div>
        <p className="text-xs text-slate-400">
          Testing whether scientific conclusions remain stable under alternative methodological choices (e.g. baseline periods and wet-day thresholds).
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sensitivityScenarios.slice(0, 4).map((scen, idx) => (
            <div key={idx} className="bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-200">{scen.district} • {scen.parameter}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${scen.trend_concordance ? 'bg-emerald-950 text-emerald-300' : 'bg-amber-950 text-amber-300'}`}>
                  {scen.trend_concordance ? 'Concordant' : 'Sensitive'}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] pt-1">
                <div className="p-2 bg-slate-900 rounded border border-slate-800">
                  <span className="text-slate-400 block">{scen.scenario_a?.name}:</span>
                  <span className="font-mono text-cyan-300">P95 = {scen.scenario_a?.threshold_p95_mm} mm</span>
                  <span className="text-[10px] text-slate-400 block">p = {scen.scenario_a?.p_value}</span>
                </div>
                <div className="p-2 bg-slate-900 rounded border border-slate-800">
                  <span className="text-slate-400 block">{scen.scenario_b?.name}:</span>
                  <span className="font-mono text-cyan-300">P95 = {scen.scenario_b?.threshold_p95_mm} mm</span>
                  <span className="text-[10px] text-slate-400 block">p = {scen.scenario_b?.p_value}</span>
                </div>
              </div>

              <p className="text-[11px] text-slate-300 italic pt-1">
                Conclusion: {scen.conclusion}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
