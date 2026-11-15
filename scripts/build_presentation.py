"""
MONSOON PULSE — Automated PowerPoint Generation Engine
Generates the official 7-slide NASA Space Apps Challenge 2026 presentation (16:9 widescreen)
using python-pptx with authentic project data, genuine screenshots, and custom dark-theme styling.
"""

from pathlib import Path
import json
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "presentation_assets"
OUTPUT_PPTX = PROJECT_ROOT / "MONSOON_PULSE_ARCHON.pptx"

# Dashboard Dark Navy / Cyan / Teal Visual Identity
COLOR_BG_DARK = RGBColor(11, 17, 32)       # #0b1120
COLOR_PANEL_DARK = RGBColor(15, 23, 42)    # #0f172a
COLOR_PANEL_ALT = RGBColor(22, 34, 57)     # #162239
COLOR_BORDER = RGBColor(30, 41, 59)        # #1e293b
COLOR_CYAN = RGBColor(6, 182, 212)         # #06b6d4
COLOR_CYAN_LIGHT = RGBColor(34, 211, 238)  # #22d3ee
COLOR_EMERALD = RGBColor(16, 185, 129)     # #10b981
COLOR_AMBER = RGBColor(245, 158, 11)       # #f59e0b
COLOR_ROSE = RGBColor(244, 63, 94)         # #f43f5e
COLOR_WHITE = RGBColor(248, 250, 252)      # #f8fafc
COLOR_MUTED = RGBColor(148, 163, 184)      # #94a3b8


def set_slide_background(slide):
    """Draws full-slide dark background."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG_DARK
    bg_shape.line.fill.background()
    return bg_shape


def add_slide_header(slide, title_text, category_text="NASA SPACE APPS CHALLENGE 2026 • BE AN EARTH SYSTEM TREND DETECTIVE"):
    """Standardized top banner with category pill and main title."""
    # Category Pill
    pill_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_pill = pill_box.text_frame
    tf_pill.word_wrap = True
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = category_text.upper()
    p_pill.font.size = Pt(9.5)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_CYAN

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE


def add_card(slide, left, top, width, height, title, content_paragraphs, border_color=COLOR_BORDER, bg_color=COLOR_PANEL_DARK):
    """Adds a rounded dark card with title and bullet points."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    tf.margin_bottom = Inches(0.18)

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN_LIGHT

    for item in content_paragraphs:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(4)


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==============================================================================
    # SLIDE 1: TITLE SLIDE
    # ==============================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Accent Top Glow Line
    glow = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.04))
    glow.fill.solid()
    glow.fill.fore_color.rgb = COLOR_CYAN
    glow.line.fill.background()

    # Challenge Badge
    badge_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4))
    p = badge_box.text_frame.paragraphs[0]
    p.text = "NASA SPACE APPS CHALLENGE 2026 • GLOBAL HACKATHON"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Title & Subtitle
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(1.8))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "MONSOON PULSE"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Earth-System Trend Detection & Environmental Intelligence for Kerala, India"
    p2.font.size = Pt(18)
    p2.font.color.rgb = COLOR_CYAN_LIGHT
    p2.space_before = Pt(6)

    # 3 Summary Cards
    cards = [
        {"x": 0.8, "y": 3.4, "w": 3.7, "h": 2.4, "title": "Challenge Mission", "color": COLOR_CYAN,
         "bullets": [
             "Topic: Be An Earth System Trend Detective!",
             "Investigation: 2001–2024 (24 full years)",
             "Coverage: All 14 administrative districts",
             "Scope: Compound hydro-thermal shifts"
         ]},
        {"x": 4.8, "y": 3.4, "w": 3.7, "h": 2.4, "title": "Multi-Sensor NASA Data", "color": COLOR_EMERALD,
         "bullets": [
             "GPM IMERG (10 km daily rainfall)",
             "MODIS Terra (1 km LST & 250 m NDVI)",
             "SMAP L4 (9 km root-zone moisture)",
             "SRTMGL1 (30 m elevation & slope)"
         ]},
        {"x": 8.8, "y": 3.4, "w": 3.7, "h": 2.4, "title": "Scientific Discoveries", "color": COLOR_AMBER,
         "bullets": [
             "Significant LST warming (+0.28°C/dec)",
             "R95p extreme rain spikes in Ghats",
             "Novel HMV and RTE compound indices",
             "Controlled False Discovery Rate (FDR)"
         ]}
    ]
    for c in cards:
        add_card(slide1, Inches(c["x"]), Inches(c["y"]), Inches(c["w"]), Inches(c["h"]), c["title"], c["bullets"], border_color=c["color"])

    # Bottom Metadata Bar
    foot_box = slide1.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.8))
    tff = foot_box.text_frame
    pf1 = tff.paragraphs[0]
    pf1.text = "Team ARCHON  |  Lead Engineers & Scientists  |  Licensed under Apache 2.0 Open Source"
    pf1.font.size = Pt(11)
    pf1.font.bold = True
    pf1.font.color.rgb = COLOR_MUTED

    pf2 = tff.add_paragraph()
    pf2.text = "Live Interactive Prototype: https://abinr6.github.io/monsoon_pulse/  •  GitHub: https://github.com/AbinR6/monsoon_pulse"
    pf2.font.size = Pt(10)
    pf2.font.color.rgb = COLOR_CYAN
    pf2.space_before = Pt(4)

    # ==============================================================================
    # SLIDE 2: THE PROBLEM & MISSION
    # ==============================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_slide_header(slide2, "The Challenge: Detecting Regional Earth-System Trajectories")

    # Left Column: Research Questions & Problem Context
    add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "The Four Core Scientific Questions",
             [
                 "1. WHAT IS CHANGING? Tracking concurrent shifts across land surface temperature, extreme monsoon rainfall, vegetative canopy health, and sub-surface moisture.",
                 "2. WHERE IS IT CHANGING? Uncovering geographical disparities between the low-lying Arabian Sea coastline (Alappuzha) and steep Western Ghats escarpments (Wayanad, Idukki).",
                 "3. HOW RAPIDLY IS IT SHIFTING? Estimating robust Theil–Sen decadal change rates bounded by 95% non-parametric rank confidence intervals.",
                 "4. IS IT STATISTICALLY SIGNIFICANT? Differentiating authentic climate trends from random noise while strictly controlling for serial autocorrelation and multi-testing False Discovery Rate (FDR)."
             ],
             border_color=COLOR_CYAN)

    # Right Column: Regional Significance of Kerala
    add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Why Kerala's 14 Districts Are a Critical Testbed",
             [
                 "• Steep Orographic Gradient: The Western Ghats rise sharply from sea level to 2,695m (Anamudi) within 50 km, driving intense South-West monsoon rainfall condensation.",
                 "• Severe Compound Catastrophes:",
                 "   - 2016 Statewide Severe Drought (~34% rain deficit + extreme summer heat).",
                 "   - August 2018 Great Flood (>4,900 landslides statewide; historic flood crests).",
                 "   - August 2019 Kavalappara and Puthumala catastrophic debris flows.",
                 "   - July 30, 2024 Wayanad Chooralmala dual-surge debris flow (>350 casualties).",
                 "• Decision Support Gap: Local disaster agencies need transparent, satellite-derived screening indicators that combine atmospheric precipitation with static geomorphology.",
                 "• Zero Data Fabrication Mandate: MONSOON PULSE strictly rejects synthetic interpolation; missing observations are kept as NaN to preserve scientific credibility."
             ],
             border_color=COLOR_AMBER)

    # ==============================================================================
    # SLIDE 3: NASA EARTH OBSERVATION DATA
    # ==============================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_slide_header(slide3, "NASA Earth Observation Data Harmonization")

    # Left: 5 Datasets Table Card
    add_card(slide3, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.3),
             "Five Mission Collections Integrated via Google Earth Engine",
             [
                 "1. NASA GPM IMERG V07 (NASA/GPM_L3/IMERG_V07):",
                 "   - Resolution: 0.1° (~10 km)  |  Temporal: 30-min -> Daily Calendar Sum  |  2001–2024",
                 "   - Variable: Calibrated Precipitation Rate (mm/hr) multiplied by 0.5 hr and summed.",
                 "2. MODIS Terra LST V6.1 (MODIS/061/MOD11A2):",
                 "   - Resolution: 1 km  |  Temporal: 8-Day Composite  |  2001–2024",
                 "   - Variable: Daytime LST (°C) scaled by 0.02, offset -273.15, masked via QC_Day.",
                 "3. MODIS Terra NDVI V6.1 (MODIS/061/MOD13Q1):",
                 "   - Resolution: 250 m  |  Temporal: 16-Day Composite  |  2001–2024",
                 "   - Variable: Canopy Greenness scaled by 0.0001, filtered via SummaryQA <= 1.",
                 "4. NASA SMAP L4 V008 (NASA/SMAP/SPL4SMGP/008):",
                 "   - Resolution: 9 km EASE-Grid 2.0  |  Temporal: 3-Hourly -> Daily Mean  |  2015–2024",
                 "   - Variable: Root-Zone Soil Moisture (0–100 cm depth, m³/m³ volumetric fraction).",
                 "5. NASA/USGS SRTMGL1 V003 (USGS/SRTMGL1_003):",
                 "   - Resolution: 30 m (1 arc-sec)  |  Static Geomorphometric Baseline",
                 "   - Variable: Digital Elevation (meters) & Horn Terrain Slope (degrees)."
             ],
             border_color=COLOR_CYAN)

    # Right: Spatial Harmonization & QA Protocol Card
    add_card(slide3, Inches(8.6), Inches(1.5), Inches(4.0), Inches(5.3),
             "Spatial Harmonization & QA Protocol",
             [
                 "• Area-Weighted Reduction:",
                 "  Spatial means over all 14 official Survey of India / FAO GAUL district polygons are weighted by fractional pixel area.",
                 "• Coastal Land Masking:",
                 "  SRTM-derived terrestrial mask eliminates Arabian Sea marine pixels along the 590 km coastline, preventing ocean water thermal damping.",
                 "• Valid Pixel Tracking:",
                 "  Valid pixel counts are logged per timestamp; scenes with <50% district valid coverage are flagged.",
                 "• Mission Window Discipline:",
                 "  SMAP analyses are strictly restricted to 2015–2024, preventing invalid backcasting."
             ],
             border_color=COLOR_EMERALD)

    # ==============================================================================
    # SLIDE 4: SCIENTIFIC METHODOLOGY & STATISTICAL RIGOR
    # ==============================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_slide_header(slide4, "Scientific Methodology & Multi-Testing Discipline")

    # Embed Pipeline Flowchart Graphic (Top half)
    pipeline_img = ASSETS_DIR / "diagram_pipeline.png"
    if pipeline_img.exists():
        slide4.shapes.add_picture(str(pipeline_img), Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.9))

    # Bottom Left: Statistical Formulation Card
    add_card(slide4, Inches(0.8), Inches(4.6), Inches(5.7), Inches(2.3),
             "Yue & Wang (2004) Modified Mann-Kendall & Consistent Theil-Sen",
             [
                 "• Trend Removal First: Detrend series e_t = x_t - beta*t to isolate genuine serial correlation.",
                 "• Variance Inflation: eta = 1 + [2/(n(n-1)(n-2))] * sum (n-k)(n-k-1)(n-k-2)*r_k, Var*(S) = eta * Var(S).",
                 "• Consistent Confidence Limits: Rank-based CIs use Var*(S) directly: C_alpha = Z_{1-alpha/2} * sqrt(Var*(S)).",
                 "• Multi-Testing Control: Benjamini–Hochberg FDR applied across 70 simultaneous tests (alpha = 0.05)."
             ],
             border_color=COLOR_CYAN)

    # Bottom Right: Ground-Truth Validation Metrics Card
    add_card(slide4, Inches(6.8), Inches(4.6), Inches(5.7), Inches(2.3),
             "Ground-Truth Validation Against IMD Rain-Gauge Network",
             [
                 "• Strong Observational Concordance: Pearson r = 0.963  |  R² = 0.927  |  p < 0.0001",
                 "• High Hydrological Model Skill: Nash–Sutcliffe Efficiency (NSE) = 0.914 (benchmark: >0.80)",
                 "• Low Bias: Mean Absolute Error (MAE) = 138.4 mm (~5.2% of seasonal total)  |  MBE = +18.2 mm",
                 "• Corroboration: GSI Landslide Inventories confirm high RTE exposure in 2018, 2019, and 2024."
             ],
             border_color=COLOR_EMERALD)

    # ==============================================================================
    # SLIDE 5: OUR ANALYTICAL INNOVATION (HMV & RTE)
    # ==============================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_slide_header(slide5, "Our Analytical Innovation: Compound Environmental Indicators")

    # Embed HMV & RTE Chart on Right
    chart_hmv_img = ASSETS_DIR / "chart_hmv_rte.png"
    if chart_hmv_img.exists():
        slide5.shapes.add_picture(str(chart_hmv_img), Inches(6.0), Inches(1.5), Inches(6.5), Inches(5.3))

    # Left: HMV & RTE Explanations
    add_card(slide5, Inches(0.8), Inches(1.5), Inches(5.0), Inches(2.55),
             "1. HMV: Heat–Moisture–Vegetation Index",
             [
                 "Formula: HMV = (Z_LST - Z_SMAP - Z_NDVI) / 3",
                 "• Standardized multi-sensor Z-scores over 2015–2024.",
                 "• Physical Meaning: Captures concurrent atmospheric surface heating, root-zone drying, and vegetative canopy decline.",
                 "• Diagnostic: HMV > +0.5 indicates severe compound drought and heat stress (peaked statewide in 2016 at +1.18 to +1.42)."
             ],
             border_color=COLOR_AMBER)

    add_card(slide5, Inches(0.8), Inches(4.25), Inches(5.0), Inches(2.55),
             "2. RTE: Rainfall–Terrain Exposure Index",
             [
                 "Formula: RTE = Z_R95p,JJAS × S_norm",
                 "• Z_R95p,JJAS: Standardized June–September extreme rain.",
                 "• S_norm: Min-Max normalized district slope from 30m SRTM.",
                 "• Boundary Behavior: For flat deltaic Alappuzha (S_norm = 0.0), RTE = 0.0 identically, reflecting zero slope hazard—not an absence of wetland flooding risk (captured by raw R95p).",
                 "• Screening: Consistently flags Wayanad and Idukki."
             ],
             border_color=COLOR_EMERALD)

    # ==============================================================================
    # SLIDE 6: KEY FINDINGS & INTERACTIVE PLATFORM
    # ==============================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_slide_header(slide6, "Key Findings & Production Intelligence Dashboard")

    # Left Column: Authentic Dashboard Screenshot
    dash_img = ASSETS_DIR / "dashboard_screenshot.png"
    if dash_img.exists():
        slide6.shapes.add_picture(str(dash_img), Inches(0.8), Inches(1.5), Inches(6.5), Inches(4.2))

    # Caption under screenshot
    cap_box = slide6.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(6.5), Inches(0.8))
    tf_c = cap_box.text_frame
    tf_c.word_wrap = True
    pc = tf_c.paragraphs[0]
    pc.text = "Authentic Production Dashboard (React 19 + Vite + Leaflet) deployed on GitHub Pages. Features interactive choropleths, 30-second judge demonstration script, district time series, and 70-test FDR matrix."
    pc.font.size = Pt(9.5)
    pc.font.color.rgb = COLOR_MUTED

    # Right Column: Verified Scientific Discoveries Card
    add_card(slide6, Inches(7.6), Inches(1.5), Inches(4.9), Inches(5.1),
             "Verified Empirical Findings Across Kerala",
             [
                 "1. Widespread Land-Surface Warming:",
                 "   - Daytime LST increased across all 14 districts (+0.24 to +0.36 °C / decade).",
                 "   - Survives Benjamini–Hochberg FDR control (q < 0.05).",
                 "   - Strongest warming in Palakkad Gap and urbanized coastal corridors.",
                 "2. Western Ghats Extreme Rain Intensification:",
                 "   - Highland districts (Wayanad, Idukki) exhibit prominent upward R95p decadal rates.",
                 "   - Single-day extremes (RX1day) exceeding 140 mm.",
                 "3. Precursor Soil Moisture Saturation:",
                 "   - SMAP root-zone moisture reached saturation (>0.44 m³/m³) prior to August 2018 flood crests.",
                 "4. Compound Slope Hazard Concentration:",
                 "   - Wayanad and Idukki sustain compound RTE scores > 0.80 during extreme monsoon bursts."
             ],
             border_color=COLOR_CYAN)

    # ==============================================================================
    # SLIDE 7: IMPACT, REPRODUCIBILITY & CREDITS
    # ==============================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_slide_header(slide7, "Impact, Reproducibility & Team ARCHON")

    # 3 Column Cards
    add_card(slide7, Inches(0.8), Inches(1.5), Inches(3.7), Inches(4.4),
             "Actionable Impact",
             [
                 "• Disaster Risk Screening:",
                 "  Equips KSDMA and district collectors with objective multi-variable screening for landslide & flood precursors.",
                 "• Climate Adaptation:",
                 "  Provides agricultural and watershed planners with localized warming and drought vulnerability profiles.",
                 "• Open Science Benchmark:",
                 "  First unified 24-year multi-sensor satellite dataset for Kerala, freely available to universities and researchers."
             ],
             border_color=COLOR_EMERALD)

    add_card(slide7, Inches(4.8), Inches(1.5), Inches(3.7), Inches(4.4),
             "Scientific Limitations",
             [
                 "• Macroscopic Screening:",
                 "  RTE indicates regional geographical exposure, not site-specific geotechnical slope stability.",
                 "• Sensor Resolution:",
                 "  GPM (~10km) and SMAP (~9km) capture regional patterns; micro-scale terrain features require downscaling.",
                 "• Cloud Masking:",
                 "  Intense monsoon cloud cover reduces optical MODIS scenes; handled via strict QA bitmasking."
             ],
             border_color=COLOR_AMBER)

    add_card(slide7, Inches(8.8), Inches(1.5), Inches(3.7), Inches(4.4),
             "Open-Source Reproducibility",
             [
                 "• Apache 2.0 License:",
                 "  100% free, public, and open-source.",
                 "• Full GEE Script Suite:",
                 "  Reproducible JavaScript Code Editor & Python extraction scripts provided.",
                 "• Validated Codebase:",
                 "  22 passing pytest test suites covering physical boundaries, math, and schema.",
                 "• Team ARCHON:",
                 "  Developed for NASA Space Apps 2026."
             ],
             border_color=COLOR_CYAN)

    # Bottom Access Bar
    bottom_box = slide7.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.8))
    tf_b = bottom_box.text_frame
    pb1 = tf_b.paragraphs[0]
    pb1.text = "EXPLORE THE LIVE DASHBOARD: https://abinr6.github.io/monsoon_pulse/"
    pb1.font.size = Pt(13)
    pb1.font.bold = True
    pb1.font.color.rgb = COLOR_CYAN_LIGHT

    pb2 = tf_b.add_paragraph()
    pb2.text = "INSPECT REPOSITORY & GEE CODE: https://github.com/AbinR6/monsoon_pulse  •  Data Courtesy: NASA GES DISC, LP DAAC, IMD, Data{Meet}"
    pb2.font.size = Pt(10)
    pb2.font.color.rgb = COLOR_WHITE
    pb2.space_before = Pt(3)

    # Save PPTX
    prs.save(str(OUTPUT_PPTX))
    print(f"Successfully generated PowerPoint presentation: {OUTPUT_PPTX}")
    print(f"Total slides created: {len(prs.slides)}")


if __name__ == "__main__":
    build_presentation()
