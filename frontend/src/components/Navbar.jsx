import React from 'react';
import { 
  Compass, 
  MapPin, 
  CloudRain, 
  Thermometer, 
  Trees, 
  Droplets, 
  Activity, 
  Mountain, 
  BarChart3, 
  BookOpen,
  Layers,
  ChevronDown,
  GitCompare
} from 'lucide-react';

export default function Navbar({ 
  activeTab, 
  setActiveTab, 
  selectedDistrict, 
  setSelectedDistrict, 
  districtsList,
  onOpenCompare 
}) {
  const navTabs = [
    { id: 'overview', label: 'Overview', icon: Compass },
    { id: 'district-explorer', label: 'District Explorer', icon: MapPin },
    { id: 'rainfall', label: 'Rainfall & R95p', icon: CloudRain },
    { id: 'temperature', label: 'Land Temperature', icon: Thermometer },
    { id: 'vegetation', label: 'Vegetation NDVI', icon: Trees },
    { id: 'soil-moisture', label: 'Soil Moisture', icon: Droplets },
    { id: 'hmv', label: 'HMV Compound', icon: Activity },
    { id: 'rte', label: 'RTE Exposure', icon: Mountain },
    { id: 'statistics', label: 'Statistical Rigor', icon: BarChart3 },
    { id: 'methodology', label: 'Methodology & Data', icon: BookOpen },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-950/95 backdrop-blur-md border-b border-slate-800 text-slate-100">
      {/* Top Bar: Brand, Project Info & Global Controls */}
      <div className="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
        {/* Brand & Mission Tag */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-emerald-400 p-0.5 shadow-lg shadow-cyan-500/20 flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Activity className="w-5 h-5 text-cyan-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white font-mono">
                MONSOON<span className="text-cyan-400">PULSE</span>
              </h1>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800 tracking-wider">
                NASA SPACE APPS 2026
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Earth-System Trend Detection Platform • Kerala (2001–2024)
            </p>
          </div>
        </div>

        {/* Global District Selector & Compare Trigger */}
        <div className="flex items-center gap-3">
          {/* District Selector */}
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-1.5 shadow-sm">
            <MapPin className="w-4 h-4 text-cyan-400" />
            <span className="text-xs text-slate-400">District:</span>
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="bg-transparent text-sm font-semibold text-slate-100 focus:outline-none cursor-pointer pr-2"
            >
              {districtsList.map((d) => (
                <option key={d} value={d} className="bg-slate-900 text-slate-100">
                  {d}
                </option>
              ))}
            </select>
          </div>

          {/* Compare Button */}
          <button
            onClick={onOpenCompare}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-cyan-400 hover:text-cyan-300 border border-slate-700 text-xs font-semibold px-3 py-2 rounded-lg transition"
            title="Compare two districts side-by-side"
          >
            <GitCompare className="w-3.5 h-3.5" />
            <span>Compare</span>
          </button>
        </div>
      </div>

      {/* Navigation Tabs Bar */}
      <div className="border-t border-slate-900 bg-slate-950/70 overflow-x-auto scrollbar-thin">
        <div className="max-w-7xl mx-auto px-4 flex space-x-1">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-1.5 py-2.5 px-3 text-xs font-medium border-b-2 whitespace-nowrap transition ${
                  isActive
                    ? 'border-cyan-400 text-cyan-400 bg-slate-900/50'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
