"""
MONSOON PULSE — Master Scientific Pipeline Orchestration
NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!

Runs the entire scientific data engineering and statistical pipeline:
1. Ingests raw satellite records across Kerala's 14 districts.
2. Performs quality control, validity checking, completeness calculation.
3. Computes ETCCDI R95p extreme precipitation indices (annual & JJAS).
4. Aggregates MODIS LST, NDVI, and SMAP temporal time series.
5. Calculates compound HMV (Heat-Moisture-Vegetation) indicator.
6. Calculates compound RTE (Rainfall-Terrain Exposure) indicator.
7. Conducts Mann-Kendall monotonic trend tests & Theil-Sen robust slope estimation with 95% CIs.
8. Evaluates lag-1 serial autocorrelation and applies Modified Mann-Kendall where needed.
9. Performs Benjamini-Hochberg False Discovery Rate (FDR) multi-testing adjustment.
10. Executes sensitivity tests across reference baselines and thresholds.
11. Verifies JSON output against schema rules.
12. Synchronizes validated analytical artifacts with the frontend dashboard.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.export.dashboard_exporter import DashboardExporter


def main():
    print("================================================================================")
    print("MONSOON PULSE: Earth-System Trend Detection & Environmental Intelligence Engine")
    print("NASA Space Apps Challenge 2026: Be An Earth System Trend Detective!")
    print("Study Region: Kerala, India | Observation Window: 2001–2024 (SMAP: 2015–2024)")
    print("================================================================================\n")
    
    exporter = DashboardExporter()
    payload = exporter.execute_and_export()
    
    print("\n--------------------------------------------------------------------------------")
    print("PIPELINE EXECUTION SUMMARY:")
    print(f"Districts Processed: {len(payload['districts_data'])}")
    print(f"Total Statistical Tests Executed: {len(payload['all_statistical_tests'])}")
    print(f"Sensitivity Scenarios Evaluated: {len(payload['sensitivity_analysis'])}")
    print("Status: SUCCESS — Production JSON generated and synced to frontend.")
    print("================================================================================\n")


if __name__ == "__main__":
    main()
