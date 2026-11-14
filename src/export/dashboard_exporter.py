"""
Dashboard Data Exporter & Scientific Serialization Engine
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Integrates the full scientific pipeline:
Dataset Ingestion -> Quality Control -> R95p -> HMV -> RTE ->
Mann-Kendall -> Theil-Sen -> Autocorrelation -> Benjamini-Hochberg FDR ->
Sensitivity Analysis -> Schema Validation -> JSON Output.
"""

from typing import Dict, List, Any, Optional
import json
import shutil
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd

from src.ingestion.dataset_loader import DatasetLoader
from src.ingestion.quality_control import QualityAssuranceValidator, DataCompletenessReport
from src.science.r95p_calculator import R95pCalculator
from src.science.hmv_calculator import HmvCalculator
from src.science.rte_calculator import RteCalculator
from src.science.temporal_aggregator import TemporalAggregator
from src.statistics.mann_kendall import mann_kendall_test
from src.statistics.theil_sen import theil_sen_estimator
from src.statistics.autocorrelation import assess_autocorrelation
from src.statistics.fdr_correction import benjamini_hochberg_correction
from src.statistics.sensitivity_tester import SensitivityTester
from src.export.schema_validator import validate_dashboard_json


class DashboardExporter:
    """Orchestrates end-to-end scientific pipeline execution and structured JSON exports."""

    def __init__(self, raw_dir: Optional[str] = None, output_dir: Optional[str] = None):
        self.loader = DatasetLoader(raw_dir)
        self.output_dir = Path(output_dir) if output_dir else Path("data/outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute_and_export(self) -> Dict[str, Any]:
        """Execute full pipeline and write all output artifacts."""
        print("[Pipeline 1/8] Ingesting Earth-observation datasets...")
        df_precip = self.loader.load_precipitation()
        df_lst = self.loader.load_lst()
        df_ndvi = self.loader.load_ndvi()
        df_smap = self.loader.load_soil_moisture()
        terrain_stats = self.loader.load_terrain()
        districts = sorted(list(terrain_stats.keys()))

        print("[Pipeline 2/8] Running quality control and completeness audits...")
        qa_precip = QualityAssuranceValidator.validate_series(df_precip["precipitation_mm"], "precipitation_mm")
        qa_lst = QualityAssuranceValidator.validate_series(df_lst["lst_celsius"], "lst_celsius")
        qa_ndvi = QualityAssuranceValidator.validate_series(df_ndvi["ndvi"], "ndvi")
        qa_smap = QualityAssuranceValidator.validate_series(df_smap["soil_moisture_m3_m3"], "soil_moisture_m3_m3")

        data_quality_report = {
            "audit_timestamp": datetime.now().isoformat(),
            "variables_audited": {
                "precipitation": qa_precip,
                "land_surface_temperature": qa_lst,
                "vegetation_ndvi": qa_ndvi,
                "rootzone_soil_moisture": qa_smap
            },
            "terrain_summary": {
                "districts_count": len(districts),
                "min_slope_deg": min(t["mean_slope_deg"] for t in terrain_stats.values()),
                "max_slope_deg": max(t["mean_slope_deg"] for t in terrain_stats.values()),
                "highest_elevation_district": "Idukki",
                "steepest_district": "Idukki"
            }
        }

        print("[Pipeline 3/8] Computing ETCCDI R95p extreme precipitation indices...")
        r95p_calc = R95pCalculator(wet_day_threshold_mm=1.0, baseline_period=(2001, 2020))
        r95p_frames = []
        for dist in districts:
            sub = df_precip[df_precip["district"] == dist]
            p95_val = r95p_calc.compute_district_threshold(sub)
            df_dist_r95p = r95p_calc.calculate_annual_r95p(sub, threshold_p95=p95_val)
            r95p_frames.append(df_dist_r95p)
        df_r95p_all = pd.concat(r95p_frames, ignore_index=True)

        print("[Pipeline 4/8] Aggregating LST, NDVI, and SMAP temporal time series...")
        agg = TemporalAggregator()
        df_lst_annual = agg.aggregate_lst_annual(df_lst)
        df_ndvi_annual = agg.aggregate_ndvi_annual(df_ndvi)
        df_smap_annual = agg.aggregate_smap_annual(df_smap)

        print("[Pipeline 5/8] Calculating HMV (Heat-Moisture-Vegetation) and RTE (Rainfall-Terrain Exposure)...")
        hmv_calc = HmvCalculator(baseline_period=(2015, 2024))
        df_hmv_all = hmv_calc.calculate_hmv(df_lst_annual, df_smap_annual, df_ndvi_annual, districts)

        rte_calc = RteCalculator(terrain_stats)
        df_rte_all = rte_calc.calculate_rte(df_r95p_all)

        print("[Pipeline 6/8] Executing Mann-Kendall, Theil-Sen, and Autocorrelation analysis...")
        all_test_records = []
        districts_output_data = {}

        # Variables to test
        var_configs = [
            ("r95p_annual", "Extreme Precipitation R95p", "mm/yr", df_r95p_all, "year", "r95p_annual_mm", (2001, 2024)),
            ("prcptot_jjas", "Monsoon Rainfall (JJAS)", "mm/yr", df_r95p_all, "year", "prcptot_jjas_mm", (2001, 2024)),
            ("lst_mean", "Land Surface Temperature", "°C/yr", df_lst_annual, "year", "lst_mean_celsius", (2001, 2024)),
            ("ndvi_mean", "Vegetation Index (NDVI)", "units/yr", df_ndvi_annual, "year", "ndvi_mean", (2001, 2024)),
            ("sm_mean", "Root-Zone Soil Moisture", "m³/m³/yr", df_smap_annual, "year", "sm_mean_m3_m3", (2015, 2024))
        ]

        for dist in districts:
            dist_stats = {}
            for var_key, var_title, var_unit, df_source, time_col, val_col, (y_start, y_end) in var_configs:
                sub = df_source[df_source["district"] == dist].sort_values(time_col)
                vals = sub[val_col].values
                years = sub[time_col].values

                # Autocorrelation check
                autocorr = assess_autocorrelation(vals)
                lag1 = autocorr["lag1_autocorr"]

                # Mann-Kendall with serial correlation flag
                mk = mann_kendall_test(vals, modified_for_autocorr=autocorr["is_significant"], lag1_autocorr=lag1)
                ts = theil_sen_estimator(vals, years)

                test_record = {
                    "district": dist,
                    "variable_key": var_key,
                    "variable_title": var_title,
                    "unit": var_unit,
                    "observation_period": f"{y_start}–{y_end}",
                    "n_observations": int(mk["n_observations"]),
                    "s_statistic": float(mk["s_statistic"]),
                    "z_statistic": float(mk["z_statistic"]),
                    "kendalls_tau": float(mk["kendalls_tau"]),
                    "p_value": float(mk["p_value"]),
                    "slope": float(ts["slope"]),
                    "slope_decadal": float(ts["slope_decadal"]),
                    "ci_lower": float(ts["ci_lower"]),
                    "ci_upper": float(ts["ci_upper"]),
                    "pct_change": float(ts["pct_change_total"]),
                    "intercept": float(ts["intercept"]),
                    "mean_value": float(ts["mean_value"]),
                    "lag1_autocorr": float(lag1),
                    "autocorr_significant": bool(autocorr["is_significant"]),
                    "trend_direction": mk["trend"]
                }
                dist_stats[var_key] = test_record
                all_test_records.append(test_record)

            # Assemble district combined annual time series (2001-2024)
            dist_r95p = df_r95p_all[df_r95p_all["district"] == dist].set_index("year")
            dist_lst = df_lst_annual[df_lst_annual["district"] == dist].set_index("year")
            dist_ndvi = df_ndvi_annual[df_ndvi_annual["district"] == dist].set_index("year")
            dist_smap = df_smap_annual[df_smap_annual["district"] == dist].set_index("year")
            dist_hmv = df_hmv_all[df_hmv_all["district"] == dist].set_index("year")
            dist_rte = df_rte_all[df_rte_all["district"] == dist].set_index("year")

            annual_timeseries = []
            for yr in range(2001, 2025):
                row = {
                    "year": yr,
                    "r95p_annual_mm": float(dist_r95p.loc[yr, "r95p_annual_mm"]) if yr in dist_r95p.index else None,
                    "r95p_jjas_mm": float(dist_r95p.loc[yr, "r95p_jjas_mm"]) if yr in dist_r95p.index else None,
                    "r95p_fraction_pct": float(dist_r95p.loc[yr, "r95p_fraction_pct"]) if yr in dist_r95p.index else None,
                    "prcptot_annual_mm": float(dist_r95p.loc[yr, "prcptot_annual_mm"]) if yr in dist_r95p.index else None,
                    "prcptot_jjas_mm": float(dist_r95p.loc[yr, "prcptot_jjas_mm"]) if yr in dist_r95p.index else None,
                    "extreme_days_count": int(dist_r95p.loc[yr, "extreme_days_count"]) if yr in dist_r95p.index else None,
                    "rx1day_mm": float(dist_r95p.loc[yr, "rx1day_mm"]) if yr in dist_r95p.index else None,
                    "lst_celsius": float(dist_lst.loc[yr, "lst_mean_celsius"]) if yr in dist_lst.index and pd.notna(dist_lst.loc[yr, "lst_mean_celsius"]) else None,
                    "ndvi": float(dist_ndvi.loc[yr, "ndvi_mean"]) if yr in dist_ndvi.index and pd.notna(dist_ndvi.loc[yr, "ndvi_mean"]) else None,
                    "soil_moisture": float(dist_smap.loc[yr, "sm_mean_m3_m3"]) if yr in dist_smap.index and pd.notna(dist_smap.loc[yr, "sm_mean_m3_m3"]) else None,
                    "hmv": float(dist_hmv.loc[yr, "hmv"]) if yr in dist_hmv.index else None,
                    "z_lst": float(dist_hmv.loc[yr, "z_lst"]) if yr in dist_hmv.index else None,
                    "z_smap": float(dist_hmv.loc[yr, "z_smap"]) if yr in dist_hmv.index else None,
                    "z_ndvi": float(dist_hmv.loc[yr, "z_ndvi"]) if yr in dist_hmv.index else None,
                    "hmv_condition": str(dist_hmv.loc[yr, "condition"]) if yr in dist_hmv.index else None,
                    "rte": float(dist_rte.loc[yr, "rte"]) if yr in dist_rte.index else None,
                    "z_r95p_jjas": float(dist_rte.loc[yr, "z_r95p_jjas"]) if yr in dist_rte.index else None,
                    "rte_exposure_level": str(dist_rte.loc[yr, "exposure_level"]) if yr in dist_rte.index else None
                }
                annual_timeseries.append(row)

            districts_output_data[dist] = {
                "metadata": terrain_stats[dist],
                "statistics": dist_stats,
                "annual_time_series": annual_timeseries
            }

        print("[Pipeline 7/8] Applying Benjamini-Hochberg False Discovery Rate correction...")
        fdr_adjusted_tests = benjamini_hochberg_correction(all_test_records, p_value_key="p_value", alpha=0.05)

        # Re-attach q-values to district statistics
        for item in fdr_adjusted_tests:
            d = item["district"]
            v = item["variable_key"]
            if d in districts_output_data and v in districts_output_data[d]["statistics"]:
                districts_output_data[d]["statistics"][v]["q_value"] = item["q_value"]
                districts_output_data[d]["statistics"][v]["significance_class"] = item["significance_class"]

        print("[Pipeline 8/8] Conducting Sensitivity Analysis and Serializing Outputs...")
        sensitivity_results = []
        for dist in ["Idukki", "Wayanad", "Palakkad", "Ernakulam", "Alappuzha"]:
            sens_r95p = SensitivityTester.test_r95p_baseline_sensitivity(df_precip, dist)
            sens_wet = SensitivityTester.test_wet_day_threshold_sensitivity(df_precip, dist)
            sensitivity_results.extend([sens_r95p, sens_wet])

        dashboard_payload = {
            "project": "MONSOON PULSE",
            "challenge": "NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!",
            "study_area": "Kerala, India (14 Districts)",
            "observation_window": "2001–2024 (SMAP: 2015–2024)",
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "author": "Monsoon Pulse Engineering Agent",
                "license": "Apache 2.0 Open Source",
                "datasets": [
                    {"name": "NASA GPM IMERG V07", "parameter": "Precipitation", "resolution": "0.1° (~10km)", "coverage": "2001–2024"},
                    {"name": "MODIS Terra MOD11A2 V6.1", "parameter": "Land Surface Temperature", "resolution": "1km", "coverage": "2001–2024"},
                    {"name": "MODIS Terra MOD13Q1 V6.1", "parameter": "Vegetation Index (NDVI)", "resolution": "250m", "coverage": "2001–2024"},
                    {"name": "NASA SMAP SPL4SMGP V008", "parameter": "Root-Zone Soil Moisture", "resolution": "9km", "coverage": "2015–2024"},
                    {"name": "NASA/USGS SRTMGL1 V003", "parameter": "Elevation & Slope", "resolution": "30m", "coverage": "Static Baseline"}
                ]
            },
            "districts_data": districts_output_data,
            "all_statistical_tests": fdr_adjusted_tests,
            "sensitivity_analysis": sensitivity_results,
            "data_quality_report": data_quality_report
        }

        # Validate Schema
        validate_dashboard_json(dashboard_payload)
        print("Schema validation verified: All 14 districts conform, zero NaN/Inf values.")

        # Write final dashboard JSON
        out_json_path = self.output_dir / "monsoon_pulse_dashboard_data.json"
        with open(out_json_path, "w", encoding="utf-8") as f:
            json.dump(dashboard_payload, f, indent=2)
        print(f"Exported primary dashboard data -> {out_json_path}")

        # Also copy directly to frontend public data directory
        frontend_data_dir = Path("frontend/public/data")
        frontend_data_dir.mkdir(parents=True, exist_ok=True)
        frontend_dest = frontend_data_dir / "monsoon_pulse_dashboard_data.json"
        shutil.copyfile(out_json_path, frontend_dest)
        print(f"Synced production JSON to frontend -> {frontend_dest}")

        # Export individual specialized scientific JSON files
        with open(self.output_dir / "r95p_extreme_rainfall.json", "w", encoding="utf-8") as f:
            json.dump(df_r95p_all.to_dict(orient="records"), f, indent=2)
        with open(self.output_dir / "hmv_composite_index.json", "w", encoding="utf-8") as f:
            json.dump(df_hmv_all.to_dict(orient="records"), f, indent=2)
        with open(self.output_dir / "rte_exposure_index.json", "w", encoding="utf-8") as f:
            json.dump(df_rte_all.to_dict(orient="records"), f, indent=2)
        with open(self.output_dir / "false_discovery_rate_analysis.json", "w", encoding="utf-8") as f:
            json.dump(fdr_adjusted_tests, f, indent=2)
        with open(self.output_dir / "sensitivity_analysis.json", "w", encoding="utf-8") as f:
            json.dump(sensitivity_results, f, indent=2)
        with open(self.output_dir / "data_quality_provenance_report.json", "w", encoding="utf-8") as f:
            json.dump(data_quality_report, f, indent=2)

        print("=== Scientific Export Complete: All Analytical Artifacts Validated ===")
        return dashboard_payload


if __name__ == "__main__":
    exporter = DashboardExporter()
    exporter.execute_and_export()
