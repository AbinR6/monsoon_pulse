import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  AlertCircle, 
  Loader2, 
  Globe2, 
  ShieldCheck, 
  ExternalLink 
} from 'lucide-react';

import Navbar from './components/Navbar';
import DistrictCompareModal from './components/DistrictCompareModal';
import OverviewSection from './components/OverviewSection';
import DistrictExplorerSection from './components/DistrictExplorerSection';
import RainfallSection from './components/RainfallSection';
import TemperatureSection from './components/TemperatureSection';
import VegetationSection from './components/VegetationSection';
import SoilMoistureSection from './components/SoilMoistureSection';
import HmvSection from './components/HmvSection';
import RteSection from './components/RteSection';
import StatisticsSection from './components/StatisticsSection';
import MethodologySection from './components/MethodologySection';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedDistrict, setSelectedDistrict] = useState('Wayanad');
  const [isCompareOpen, setIsCompareOpen] = useState(false);

  const [dashboardData, setDashboardData] = useState(null);
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        // Load production analytical JSON and district GeoJSON
        const [dashRes, geoRes] = await Promise.all([
          fetch('/data/monsoon_pulse_dashboard_data.json'),
          fetch('/data/kerala_districts.geojson')
        ]);

        if (!dashRes.ok) {
          throw new Error(`Failed to load analytical dashboard data: HTTP ${dashRes.status}`);
        }
        if (!geoRes.ok) {
          throw new Error(`Failed to load Kerala district boundaries: HTTP ${geoRes.status}`);
        }

        const dashJson = await dashRes.json();
        const geoJson = await geoRes.json();

        setDashboardData(dashJson);
        setGeoJsonData(geoJson);
        setError(null);
      } catch (err) {
        console.error('Data loading error:', err);
        setError(err.message || 'Error loading satellite analytical data.');
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const districtsList = Object.keys(dashboardData?.districts_data || {}).sort();
  const currentDistrictData = dashboardData?.districts_data?.[selectedDistrict];

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-4">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-600 to-emerald-400 p-0.5 shadow-2xl shadow-cyan-500/20 mb-6 flex items-center justify-center">
          <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
            <Activity className="w-8 h-8 text-cyan-400 animate-pulse" />
          </div>
        </div>
        <h2 className="text-xl font-bold font-mono text-white mb-2 tracking-wide">
          INITIALIZING MONSOON PULSE OBSERVATORY
        </h2>
        <p className="text-xs text-slate-400 max-w-sm text-center mb-6">
          Ingesting calibrated NASA Earth-observation records and multi-testing statistics for Kerala's 14 districts...
        </p>
        <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-4">
        <div className="max-w-md bg-slate-900 border border-rose-800 rounded-2xl p-6 shadow-2xl text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-rose-400 mx-auto" />
          <h2 className="text-lg font-bold text-rose-300">Analytical Data Ingestion Error</h2>
          <p className="text-xs text-slate-400 leading-relaxed">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold transition"
          >
            Retry Ingestion
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-cyan-500 selection:text-slate-950">
      {/* Top Sticky Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedDistrict={selectedDistrict}
        setSelectedDistrict={setSelectedDistrict}
        districtsList={districtsList}
        onOpenCompare={() => setIsCompareOpen(true)}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6">
        {activeTab === 'overview' && (
          <OverviewSection
            dashboardData={dashboardData}
            geoJsonData={geoJsonData}
            selectedDistrict={selectedDistrict}
            setSelectedDistrict={setSelectedDistrict}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'district-explorer' && (
          <DistrictExplorerSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
            setSelectedDistrict={setSelectedDistrict}
            districtsList={districtsList}
          />
        )}

        {activeTab === 'rainfall' && (
          <RainfallSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
          />
        )}

        {activeTab === 'temperature' && (
          <TemperatureSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
          />
        )}

        {activeTab === 'vegetation' && (
          <VegetationSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
          />
        )}

        {activeTab === 'soil-moisture' && (
          <SoilMoistureSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
          />
        )}

        {activeTab === 'hmv' && (
          <HmvSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
            sensitivityData={dashboardData?.sensitivity_analysis}
          />
        )}

        {activeTab === 'rte' && (
          <RteSection
            districtData={currentDistrictData}
            selectedDistrict={selectedDistrict}
            allDistrictsData={dashboardData?.districts_data}
          />
        )}

        {activeTab === 'statistics' && (
          <StatisticsSection
            dashboardData={dashboardData}
            selectedDistrict={selectedDistrict}
            setSelectedDistrict={setSelectedDistrict}
          />
        )}

        {activeTab === 'methodology' && (
          <MethodologySection />
        )}
      </main>

      {/* District Compare Modal */}
      <DistrictCompareModal
        isOpen={isCompareOpen}
        onClose={() => setIsCompareOpen(false)}
        districtsData={dashboardData?.districts_data}
        districtsList={districtsList}
        initialDistrictA={selectedDistrict}
        initialDistrictB={selectedDistrict === 'Wayanad' ? 'Palakkad' : 'Wayanad'}
      />

      {/* Mission Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/90 py-6 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="font-mono font-bold text-slate-200">MONSOON PULSE</span> • NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!
            <p className="text-[11px] text-slate-500 mt-0.5">
              Powered by NASA GPM IMERG, MODIS Terra (MOD11A2 & MOD13Q1), SMAP (SPL4SMGP), and SRTMGL1 V003.
            </p>
          </div>

          <div className="flex items-center gap-4 text-[11px]">
            <a
              href="https://www.spaceappschallenge.org/2026/challenges/earth-system-trend-detective/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-cyan-400 transition inline-flex items-center gap-1"
            >
              <span>NASA Challenge Page</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <span className="text-slate-700">|</span>
            <span className="text-slate-400">Apache 2.0 Open Source</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
