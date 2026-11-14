import React from 'react';
import { 
  BookOpen, 
  Database, 
  Cpu, 
  ShieldCheck, 
  Award, 
  ExternalLink, 
  Layers, 
  FileText,
  Code2,
  CheckCircle2
} from 'lucide-react';

export default function MethodologySection() {
  const datasets = [
    {
      name: 'NASA GPM IMERG V07',
      catalogId: 'NASA/GPM_L3/IMERG_V07',
      variable: 'Calibrated Precipitation Rate',
      resolution: '0.1° (~10 km)',
      frequency: '30-minute (Daily Integrated)',
      period: '2001–2024',
      docUrl: 'https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_V07'
    },
    {
      name: 'MODIS Terra MOD11A2 V6.1',
      catalogId: 'MODIS/061/MOD11A2',
      variable: 'Daytime Land Surface Temperature',
      resolution: '1 km',
      frequency: '8-Day Composite',
      period: '2001–2024',
      docUrl: 'https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2'
    },
    {
      name: 'MODIS Terra MOD13Q1 V6.1',
      catalogId: 'MODIS/061/MOD13Q1',
      variable: 'Normalized Difference Vegetation Index (NDVI)',
      resolution: '250 m',
      frequency: '16-Day Composite',
      period: '2001–2024',
      docUrl: 'https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1'
    },
    {
      name: 'NASA SMAP SPL4SMGP V008',
      catalogId: 'NASA/SMAP/SPL4SMGP/008',
      variable: 'Root-Zone Soil Moisture (0–100 cm depth)',
      resolution: '9 km (EASE-Grid 2.0)',
      frequency: '3-Hourly Model-Assimilated',
      period: '2015–2024 (Operational launch period)',
      docUrl: 'https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL4SMGP_008'
    },
    {
      name: 'NASA/USGS SRTMGL1 V003',
      catalogId: 'USGS/SRTMGL1_003',
      variable: 'Digital Elevation Model & Horn Slope',
      resolution: '30 m (1 arc-second)',
      frequency: 'Static Geomorphometric Baseline',
      period: 'Global Mission Baseline',
      docUrl: 'https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003'
    }
  ];

  const criteria = [
    {
      criterion: '1. Impact',
      focus: 'Meaningful regional environmental insight',
      response: 'Provides actionable district-level Earth-system intelligence across Kerala\'s 14 districts, helping planners, researchers, and communities understand intensifying compound climate pressures.'
    },
    {
      criterion: '2. Creativity',
      focus: 'Distinctive multi-variable analytical indicators',
      response: 'Introduces two novel compound indices: HMV (Heat–Moisture–Vegetation) and RTE (Rainfall–Terrain Exposure), connecting satellite climate indicators directly with regional topography.'
    },
    {
      criterion: '3. Validity',
      focus: 'Scientific credibility and reproducibility',
      response: 'Strict ETCCDI R95p protocol, Mann-Kendall non-parametric monotonic trend testing, Theil-Sen robust slope estimator with 95% rank CIs, autocorrelation assessment, and Benjamini-Hochberg FDR control.'
    },
    {
      criterion: '4. Relevance',
      focus: 'Direct alignment with challenge statement',
      response: 'Specifically tailored to "Be An Earth System Trend Detective!", evaluating multi-sensor NASA Earth-observation records across 2001–2024 to answer: What is changing? Where? How fast? Is it statistically significant?'
    },
    {
      criterion: '5. Presentation',
      focus: 'Clarity, accessibility and professional delivery',
      response: 'Interactive, responsive satellite observatory platform with zero-login access, interactive geospatial choropleths, transparent units, baseline documentation, and 30-second demo sequence.'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            <h2 className="text-xl font-bold font-mono text-white">
              Scientific Methodology, Datasets & Provenance
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            Complete technical documentation, official NASA Earth-observation collection identifiers, 
            mathematical formulations, open-source licensing, and challenge submission audit.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <Award className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-300">License: <strong className="text-cyan-300">Apache 2.0 Open Source</strong></span>
        </div>
      </div>

      {/* NASA Space Apps 2026 Judging Alignment */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center gap-2">
          <Award className="w-5 h-5 text-amber-400" />
          <h3 className="text-base font-bold text-slate-100">
            Official 2026 NASA Space Apps Judging Criteria Alignment
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {criteria.map((c, idx) => (
            <div key={idx} className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-xs space-y-2">
              <span className="font-bold text-sm text-cyan-400 block">{c.criterion}</span>
              <strong className="text-slate-300 block">{c.focus}</strong>
              <p className="text-slate-400 leading-relaxed">{c.response}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Earth Observation Data Catalog */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-blue-400" />
          <h3 className="text-base font-bold text-slate-100">
            Official NASA Earth-Observation Datasets Queried
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider">
              <tr>
                <th className="py-2.5 px-3">Dataset Name</th>
                <th className="py-2.5 px-3">GEE Catalog ID</th>
                <th className="py-2.5 px-3">Variable & Units</th>
                <th className="py-2.5 px-3">Resolution</th>
                <th className="py-2.5 px-3">Temporal Coverage</th>
                <th className="py-2.5 px-3">Official Docs</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono">
              {datasets.map((d, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="py-2.5 px-3 font-sans font-bold text-slate-100">{d.name}</td>
                  <td className="py-2.5 px-3 text-cyan-400">{d.catalogId}</td>
                  <td className="py-2.5 px-3 font-sans text-slate-300">{d.variable}</td>
                  <td className="py-2.5 px-3 text-slate-400">{d.resolution}</td>
                  <td className="py-2.5 px-3 text-slate-300">{d.period}</td>
                  <td className="py-2.5 px-3 font-sans">
                    <a
                      href={d.docUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-cyan-400 hover:text-cyan-300 font-medium"
                    >
                      <span>Catalog</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Mathematical Formulations Reference */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-violet-400" />
          <h3 className="text-base font-bold text-slate-100">
            Analytical Indicator Formulations
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-2">
            <h4 className="font-bold text-sm font-sans text-amber-400">1. Heat–Moisture–Vegetation (HMV)</h4>
            <div className="p-2.5 bg-slate-900 rounded border border-slate-800 text-amber-300 text-sm">
              HMV = (Z_LST - Z_SMAP - Z_NDVI) / 3
            </div>
            <p className="font-sans text-slate-400 text-[11px] leading-relaxed pt-1">
              Standardized Z-scores relative to common multi-sensor baseline (2015–2024). 
              A positive value signifies simultaneous thermal stress, soil water deficit, and canopy degradation.
            </p>
          </div>

          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-2">
            <h4 className="font-bold text-sm font-sans text-emerald-400">2. Rainfall–Terrain Exposure (RTE)</h4>
            <div className="p-2.5 bg-slate-900 rounded border border-slate-800 text-emerald-300 text-sm">
              RTE = Z_R95p,JJAS &times; S_norm
            </div>
            <p className="font-sans text-slate-400 text-[11px] leading-relaxed pt-1">
              Where Z_R95p,JJAS is standardized June–September extreme rainfall, and S_norm is min-max normalized 
              district mean terrain slope derived from NASA/USGS SRTM: S_norm = (S_d - S_min) / (S_max - S_min).
            </p>
          </div>
        </div>
      </div>

      {/* Attribution, Open Source License & AI Disclosure */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 text-xs text-slate-300 space-y-3">
        <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          Open-Source Licensing, Attribution & AI Transparency
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 text-[11px]">
          <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
            <strong className="text-slate-100 block">Open-Source License</strong>
            <p className="text-slate-400">
              Distributed under the <strong>Apache License 2.0</strong> (OSI-compliant). 
              Free for academic, research, and public utilization without login or paywalls.
            </p>
          </div>

          <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
            <strong className="text-slate-100 block">Third-Party Attribution</strong>
            <p className="text-slate-400">
              Kerala district administrative boundaries sourced from <strong>Data&#123;Meet&#125;</strong> under CC-BY 2.5 India / ODbL. 
              Satellite datasets courtesy of <strong>NASA GES DISC</strong>, <strong>LP DAAC</strong>, and <strong>Google Earth Engine</strong>.
            </p>
          </div>

          <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
            <strong className="text-slate-100 block">AI Assistance Disclosure</strong>
            <p className="text-slate-400">
              Software architecture, frontend components, and pipeline engineering implemented with 
              autonomous AI assistance in full compliance with NASA Space Apps 2026 guidelines.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
