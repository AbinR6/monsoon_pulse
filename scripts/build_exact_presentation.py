"""
MONSOON PULSE — Exact 7-Slide PowerPoint Presentation Generator
Builds MONSOON_PULSE_ARCHON.pptx with exact user-supplied text verbatim,
using widescreen 16:9 layout and professional dark-navy/cyan geospatial aesthetic.
"""

from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PPTX = PROJECT_ROOT / "MONSOON_PULSE_ARCHON.pptx"

# Exact Color Palette (Dark Navy, Cyan, Teal, Amber)
C_BG_DARK = RGBColor(11, 17, 32)       # #0b1120
C_PANEL_DARK = RGBColor(15, 23, 42)    # #0f172a
C_PANEL_ALT = RGBColor(22, 34, 57)     # #162239
C_BORDER = RGBColor(30, 41, 59)        # #1e293b
C_CYAN = RGBColor(6, 182, 212)         # #06b6d4
C_CYAN_LIGHT = RGBColor(34, 211, 238)  # #22d3ee
C_EMERALD = RGBColor(16, 185, 129)     # #10b981
C_AMBER = RGBColor(245, 158, 11)       # #f59e0b
C_ROSE = RGBColor(244, 63, 94)         # #f43f5e
C_WHITE = RGBColor(248, 250, 252)      # #f8fafc
C_MUTED = RGBColor(148, 163, 184)      # #94a3b8


def set_slide_background(slide):
    """Draws full-bleed background."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG_DARK
    bg.line.fill.background()
    return bg


def add_header(slide, slide_num_str, title_text, subtitle_text):
    """Adds standardized header tracking row, slide title, and subtitle."""
    # Top Tracker Row
    tracker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.3))
    tf_tr = tracker_box.text_frame
    tf_tr.word_wrap = True
    p_tr = tf_tr.paragraphs[0]
    p_tr.text = f"MONSOON PULSE • ARCHON                    {slide_num_str}"
    p_tr.font.size = Pt(10)
    p_tr.font.bold = True
    p_tr.font.color.rgb = C_CYAN

    # Title Box
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.6))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    pt = tf_t.paragraphs[0]
    pt.text = title_text
    pt.font.size = Pt(22)
    pt.font.bold = True
    pt.font.color.rgb = C_WHITE

    # Subtitle Box
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.4))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    ps = tf_s.paragraphs[0]
    ps.text = subtitle_text
    ps.font.size = Pt(12)
    ps.font.color.rgb = C_CYAN_LIGHT


def add_styled_panel(slide, left, top, width, height, border_color=C_BORDER, bg_color=C_PANEL_DARK):
    """Adds a dark panel container with border."""
    panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    panel.fill.solid()
    panel.fill.fore_color.rgb = bg_color
    panel.line.color.rgb = border_color
    panel.line.width = Pt(1.5)
    return panel


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ==============================================================================
    # SLIDE 1 (01 / 07): TITLE SLIDE
    # ==============================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_background(s1)

    # Top tracker
    tr1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
    p_tr1 = tr1.text_frame.paragraphs[0]
    p_tr1.text = "MONSOON PULSE • ARCHON                    01 / 07"
    p_tr1.font.size = Pt(10)
    p_tr1.font.bold = True
    p_tr1.font.color.rgb = C_CYAN

    # Banner Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = C_PANEL_ALT
    pill.line.color.rgb = C_CYAN
    pill.line.width = Pt(1)
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "NASA SPACE APPS CHALLENGE 2026 • BE AN EARTH SYSTEM TREND DETECTIVE!"
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = C_CYAN_LIGHT
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Hero Box
    hero = add_styled_panel(s1, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3), border_color=C_BORDER, bg_color=C_PANEL_DARK)
    tf_h = hero.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = Inches(0.4)
    tf_h.margin_right = Inches(0.4)
    tf_h.margin_top = Inches(0.35)

    ph1 = tf_h.paragraphs[0]
    ph1.text = "MONSOON PULSE"
    ph1.font.size = Pt(40)
    ph1.font.bold = True
    ph1.font.color.rgb = C_WHITE

    ph2 = tf_h.add_paragraph()
    ph2.text = "Earth-System Trend Detection for Kerala | 2001–2024"
    ph2.font.size = Pt(18)
    ph2.font.bold = True
    ph2.font.color.rgb = C_CYAN_LIGHT
    ph2.space_before = Pt(8)

    ph3 = tf_h.add_paragraph()
    ph3.text = "TEAM ARCHON"
    ph3.font.size = Pt(16)
    ph3.font.bold = True
    ph3.font.color.rgb = C_EMERALD
    ph3.space_before = Pt(14)

    ph4 = tf_h.add_paragraph()
    ph4.text = "A district-scale platform to explore long-term environmental change across Kerala’s 14 districts."
    ph4.font.size = Pt(13)
    ph4.font.color.rgb = C_WHITE
    ph4.space_before = Pt(14)

    ph5 = tf_h.add_paragraph()
    ph5.text = "Combines precipitation, land-surface temperature, vegetation, root-zone soil moisture and terrain."
    ph5.font.size = Pt(13)
    ph5.font.color.rgb = C_MUTED
    ph5.space_before = Pt(6)

    # Links Box at bottom
    link_panel = add_styled_panel(s1, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8), border_color=C_CYAN, bg_color=C_PANEL_ALT)
    tf_l = link_panel.text_frame
    tf_l.word_wrap = True
    pl = tf_l.paragraphs[0]
    pl.text = "Prototype: https://abinr6.github.io/monsoon_pulse/  |  Code: https://github.com/AbinR6/monsoon_pulse"
    pl.font.size = Pt(12)
    pl.font.bold = True
    pl.font.color.rgb = C_WHITE
    pl.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 2 (02 / 07): THE QUESTION: WHAT IS CHANGING ACROSS KERALA?
    # ==============================================================================
    s2 = prs.slides.add_slide(blank)
    set_slide_background(s2)
    add_header(s2, "02 / 07", "The question: what is changing across Kerala?", "A 24-year Earth-observation investigation at district scale")

    # 4 Question Cards
    q_items = [
        ("• WHAT is changing?", "Track long-term trajectories in rainfall extremes, daytime land-surface temperature and vegetation.", C_CYAN),
        ("• WHERE is it changing?", "Compare all 14 districts and examine coastal, midland and highland settings.", C_EMERALD),
        ("• HOW FAST is it changing?", "Estimate monotonic trends and robust rates of change.", C_AMBER),
        ("• IS IT STATISTICALLY DEFENSIBLE?", "Report uncertainty and control false discoveries across multiple tests.", C_CYAN_LIGHT)
    ]

    for idx, (head, body, color) in enumerate(q_items):
        top_pos = Inches(1.8 + idx * 1.05)
        panel = add_styled_panel(s2, Inches(0.8), top_pos, Inches(11.733), Inches(0.92), border_color=color, bg_color=C_PANEL_DARK)
        tf_q = panel.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = Inches(0.25)
        tf_q.margin_top = Inches(0.12)

        pq1 = tf_q.paragraphs[0]
        pq1.text = head
        pq1.font.size = Pt(13)
        pq1.font.bold = True
        pq1.font.color.rgb = color

        pq2 = tf_q.add_paragraph()
        pq2.text = body
        pq2.font.size = Pt(11)
        pq2.font.color.rgb = C_WHITE
        pq2.space_before = Pt(2)

    # Bottom summary box
    bot_s2 = add_styled_panel(s2, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.75), border_color=C_BORDER, bg_color=C_PANEL_ALT)
    tf_b2 = bot_s2.text_frame
    tf_b2.word_wrap = True
    pb2 = tf_b2.paragraphs[0]
    pb2.text = "Kerala’s Western Ghats, monsoon exposure and elevation gradients make spatially resolved environmental analysis especially relevant."
    pb2.font.size = Pt(11)
    pb2.font.color.rgb = C_WHITE
    pb2.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 3 (03 / 07): FIVE EARTH-OBSERVATION DATASETS
    # ==============================================================================
    s3 = prs.slides.add_slide(blank)
    set_slide_background(s3)
    add_header(s3, "03 / 07", "Five Earth-observation datasets", "Documented data architecture and observation windows")

    # Table Shape
    rows = 6
    cols = 3
    left = Inches(0.8)
    top = Inches(1.75)
    width = Inches(11.733)
    height = Inches(4.2)

    table_shape = s3.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(3.8)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(3.433)

    table_data = [
        ["Dataset / collection", "Variable", "Resolution / coverage"],
        ["NASA GPM IMERG V07", "Precipitation", "0.1°; 2001–2024"],
        ["MODIS Terra MOD11A2 V6.1", "Daytime land-surface temperature", "1 km; 2001–2024"],
        ["MODIS Terra MOD13Q1 V6.1", "Vegetation index (NDVI)", "250 m; 2001–2024"],
        ["NASA SMAP SPL4SMGP V008", "Root-zone soil moisture (0–100 cm)", "~9 km; 2015–2024"],
        ["NASA/USGS SRTMGL1 V003", "Elevation and terrain slope", "~30 m; global mission baseline"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_CYAN_LIGHT
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_PANEL_ALT
            else:
                p.font.color.rgb = C_WHITE if c_idx == 0 else C_MUTED
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_PANEL_DARK if r_idx % 2 == 1 else C_PANEL_ALT

    # Bottom Note
    bot_s3 = add_styled_panel(s3, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.75), border_color=C_BORDER, bg_color=C_PANEL_ALT)
    tf_b3 = bot_s3.text_frame
    tf_b3.word_wrap = True
    pb3 = tf_b3.paragraphs[0]
    pb3.text = "SMAP begins in 2015. The three-variable HMV composite therefore uses the common 2015–2024 observation window."
    pb3.font.size = Pt(11)
    pb3.font.color.rgb = C_CYAN_LIGHT
    pb3.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 4 (04 / 07): FROM OBSERVATIONS TO TREND EVIDENCE
    # ==============================================================================
    s4 = prs.slides.add_slide(blank)
    set_slide_background(s4)
    add_header(s4, "04 / 07", "From observations to trend evidence", "A reproducible analysis pathway")

    # 6 Steps in a 3x2 Grid
    steps = [
        ("01", "ACQUIRE", "Retrieve Earth-observation products and Kerala district boundaries.", C_CYAN),
        ("02", "PREPARE", "Apply quality information, spatial aggregation and temporal summaries.", C_CYAN_LIGHT),
        ("03", "DERIVE", "Calculate annual / seasonal indicators, including R95p.", C_EMERALD),
        ("04", "TEST", "Estimate Mann–Kendall trends and Theil–Sen slopes with confidence intervals.", C_AMBER),
        ("05", "CONTROL", "Apply Benjamini–Hochberg false-discovery-rate adjustment.", C_ROSE),
        ("06", "EXPLORE", "Present district comparisons, time series, maps and methodology.", C_WHITE)
    ]

    card_w = Inches(3.7)
    card_h = Inches(2.0)
    for idx, (num, tag, desc, color) in enumerate(steps):
        row = idx // 3
        col = idx % 3
        c_left = Inches(0.8 + col * 4.01)
        c_top = Inches(1.75 + row * 2.2)

        pnl = add_styled_panel(s4, c_left, c_top, card_w, card_h, border_color=color, bg_color=C_PANEL_DARK)
        tf_st = pnl.text_frame
        tf_st.word_wrap = True
        tf_st.margin_left = Inches(0.2)
        tf_st.margin_top = Inches(0.18)

        pst1 = tf_st.paragraphs[0]
        pst1.text = f"{num}  {tag}"
        pst1.font.size = Pt(13)
        pst1.font.bold = True
        pst1.font.color.rgb = color

        pst2 = tf_st.add_paragraph()
        pst2.text = desc
        pst2.font.size = Pt(10.5)
        pst2.font.color.rgb = C_WHITE
        pst2.space_before = Pt(6)

    # Bottom Note
    bot_s4 = add_styled_panel(s4, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.75), border_color=C_BORDER, bg_color=C_PANEL_ALT)
    tf_b4 = bot_s4.text_frame
    tf_b4.word_wrap = True
    pb4 = tf_b4.paragraphs[0]
    pb4.text = "The repository includes GEE scripts and Python analysis modules. Extraction/export provenance for each time-series product should be documented with the submitted data."
    pb4.font.size = Pt(10.5)
    pb4.font.color.rgb = C_MUTED
    pb4.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 5 (05 / 07): TWO PROJECT-DEFINED COMPOUND INDICATORS
    # ==============================================================================
    s5 = prs.slides.add_slide(blank)
    set_slide_background(s5)
    add_header(s5, "05 / 07", "Two project-defined compound indicators", "Complementary views of environmental conditions and terrain exposure")

    # Card 1: HMV
    panel_hmv = add_styled_panel(s5, Inches(0.8), Inches(1.8), Inches(5.65), Inches(4.2), border_color=C_AMBER, bg_color=C_PANEL_DARK)
    tf_hmv = panel_hmv.text_frame
    tf_hmv.word_wrap = True
    tf_hmv.margin_left = Inches(0.3)
    tf_hmv.margin_right = Inches(0.3)
    tf_hmv.margin_top = Inches(0.25)

    phmv1 = tf_hmv.paragraphs[0]
    phmv1.text = "HMV | HEAT–MOISTURE–VEGETATION"
    phmv1.font.size = Pt(14)
    phmv1.font.bold = True
    phmv1.font.color.rgb = C_AMBER

    phmv2 = tf_hmv.add_paragraph()
    phmv2.text = "HMV = (Z_LST − Z_SMAP − Z_NDVI) / 3"
    phmv2.font.size = Pt(13)
    phmv2.font.bold = True
    phmv2.font.color.rgb = C_CYAN_LIGHT
    phmv2.space_before = Pt(8)

    phmv3 = tf_hmv.add_paragraph()
    phmv3.text = "Combines standardized land-surface temperature, root-zone soil moisture and vegetation. Positive values indicate a warmer / drier / less-green combination relative to the selected baseline."
    phmv3.font.size = Pt(11)
    phmv3.font.color.rgb = C_WHITE
    phmv3.space_before = Pt(12)

    # Card 2: RTE
    panel_rte = add_styled_panel(s5, Inches(6.88), Inches(1.8), Inches(5.65), Inches(4.2), border_color=C_EMERALD, bg_color=C_PANEL_DARK)
    tf_rte = panel_rte.text_frame
    tf_rte.word_wrap = True
    tf_rte.margin_left = Inches(0.3)
    tf_rte.margin_right = Inches(0.3)
    tf_rte.margin_top = Inches(0.25)

    prte1 = tf_rte.paragraphs[0]
    prte1.text = "RTE | RAINFALL–TERRAIN EXPOSURE"
    prte1.font.size = Pt(14)
    prte1.font.bold = True
    prte1.font.color.rgb = C_EMERALD

    prte2 = tf_rte.add_paragraph()
    prte2.text = "RTE = Z_R95p,JJAS × S_norm"
    prte2.font.size = Pt(13)
    prte2.font.bold = True
    prte2.font.color.rgb = C_CYAN_LIGHT
    prte2.space_before = Pt(8)

    prte3 = tf_rte.add_paragraph()
    prte3.text = "Combines standardized June–September extreme rainfall with normalized terrain slope. It is a geographic screening index, not a landslide probability."
    prte3.font.size = Pt(11)
    prte3.font.color.rgb = C_WHITE
    prte3.space_before = Pt(12)

    # Bottom Note
    bot_s5 = add_styled_panel(s5, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.75), border_color=C_BORDER, bg_color=C_PANEL_ALT)
    tf_b5 = bot_s5.text_frame
    tf_b5.word_wrap = True
    pb5 = tf_b5.paragraphs[0]
    pb5.text = "HMV uses the shared 2015–2024 multi-sensor period. RTE classifications and thresholds are project-defined screening categories."
    pb5.font.size = Pt(11)
    pb5.font.color.rgb = C_CYAN_LIGHT
    pb5.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 6 (06 / 07): WHAT THE PLATFORM LETS USERS INVESTIGATE
    # ==============================================================================
    s6 = prs.slides.add_slide(blank)
    set_slide_background(s6)
    add_header(s6, "06 / 07", "What the platform lets users investigate", "A district-focused interface for transparent exploration")

    # 6 Modules in 3x2 Grid
    modules = [
        ("DISTRICT EXPLORER", "Select districts and compare terrain context and environmental trajectories.", C_CYAN),
        ("RAINFALL & R95p", "Inspect annual / monsoon precipitation and extreme-rainfall indicators.", C_CYAN_LIGHT),
        ("LAND TEMPERATURE & NDVI", "Explore daytime surface-temperature and vegetation time series.", C_ROSE),
        ("SOIL MOISTURE & HMV", "Review the 2015–2024 SMAP window and the three-variable composite.", C_AMBER),
        ("RTE EXPOSURE", "Compare standardized extreme rainfall with normalized slope.", C_EMERALD),
        ("STATISTICAL RIGOR", "Inspect trend estimates, confidence intervals, raw p-values and FDR-adjusted q-values.", C_WHITE)
    ]

    for idx, (m_tag, m_desc, m_color) in enumerate(modules):
        row = idx // 3
        col = idx % 3
        m_left = Inches(0.8 + col * 4.01)
        m_top = Inches(1.75 + row * 2.2)

        mpnl = add_styled_panel(s6, m_left, m_top, Inches(3.7), Inches(2.0), border_color=m_color, bg_color=C_PANEL_DARK)
        tf_m = mpnl.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = Inches(0.2)
        tf_m.margin_top = Inches(0.18)

        pm1 = tf_m.paragraphs[0]
        pm1.text = m_tag
        pm1.font.size = Pt(12)
        pm1.font.bold = True
        pm1.font.color.rgb = m_color

        pm2 = tf_m.add_paragraph()
        pm2.text = m_desc
        pm2.font.size = Pt(10.5)
        pm2.font.color.rgb = C_WHITE
        pm2.space_before = Pt(6)

    # Bottom Note
    bot_s6 = add_styled_panel(s6, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.75), border_color=C_BORDER, bg_color=C_PANEL_ALT)
    tf_b6 = bot_s6.text_frame
    tf_b6.word_wrap = True
    pb6 = tf_b6.paragraphs[0]
    pb6.text = "An exploratory historical analysis platform: interpret findings alongside observation windows, data quality and statistical significance."
    pb6.font.size = Pt(10.5)
    pb6.font.color.rgb = C_MUTED
    pb6.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 7 (07 / 07): IMPACT, TRANSPARENCY & NEXT STEPS
    # ==============================================================================
    s7 = prs.slides.add_slide(blank)
    set_slide_background(s7)
    add_header(s7, "07 / 07", "Impact, transparency & next steps", "Open methods and responsible interpretation")

    # Main Top Box: 5 Bullets
    panel_s7 = add_styled_panel(s7, Inches(0.8), Inches(1.7), Inches(11.733), Inches(3.3), border_color=C_BORDER, bg_color=C_PANEL_DARK)
    tf_s7 = panel_s7.text_frame
    tf_s7.word_wrap = True
    tf_s7.margin_left = Inches(0.3)
    tf_s7.margin_right = Inches(0.3)
    tf_s7.margin_top = Inches(0.18)

    bullets_s7 = [
        "• Potential users: researchers, planners and disaster-risk practitioners examining district-level environmental change.",
        "• Reproducibility: public source code, documented formulas, dataset identifiers and statistical outputs.",
        "• Interpretation: distinguish FDR-significant trends, unadjusted-only results, non-significant trends and project-defined exposure classes.",
        "• Data provenance: publish extraction dates, GEE export tasks, processing parameters, missing-data checks and source files for every dataset.",
        "• Validation: document independent gauge comparisons with station coverage, period, metrics and reproducible calculations."
    ]

    for idx, b_text in enumerate(bullets_s7):
        p_b = tf_s7.paragraphs[0] if idx == 0 else tf_s7.add_paragraph()
        p_b.text = b_text
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_WHITE
        p_b.space_before = Pt(4)

    # Bottom Credits Panel
    credits_panel = add_styled_panel(s7, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.9), border_color=C_CYAN, bg_color=C_PANEL_ALT)
    tf_cr = credits_panel.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = Inches(0.3)
    tf_cr.margin_right = Inches(0.3)
    tf_cr.margin_top = Inches(0.18)

    pcr1 = tf_cr.paragraphs[0]
    pcr1.text = "DATA & SOFTWARE CREDITS"
    pcr1.font.size = Pt(12)
    pcr1.font.bold = True
    pcr1.font.color.rgb = C_CYAN_LIGHT

    pcr2 = tf_cr.add_paragraph()
    pcr2.text = "NASA GPM IMERG • MODIS Terra • NASA SMAP • NASA/USGS SRTM"
    pcr2.font.size = Pt(10.5)
    pcr2.font.color.rgb = C_WHITE
    pcr2.space_before = Pt(3)

    pcr3 = tf_cr.add_paragraph()
    pcr3.text = "Google Earth Engine • DataMeet administrative boundaries (as attributed in project materials)"
    pcr3.font.size = Pt(10.5)
    pcr3.font.color.rgb = C_MUTED
    pcr3.space_before = Pt(2)

    pcr4 = tf_cr.add_paragraph()
    pcr4.text = "Team ARCHON • Apache License 2.0 (repository declaration)"
    pcr4.font.size = Pt(10.5)
    pcr4.font.bold = True
    pcr4.font.color.rgb = C_EMERALD
    pcr4.space_before = Pt(2)

    pcr5 = tf_cr.add_paragraph()
    pcr5.text = "Prototype and repository links are listed in the submission text."
    pcr5.font.size = Pt(10)
    pcr5.font.color.rgb = C_CYAN
    pcr5.space_before = Pt(3)

    prs.save(str(OUTPUT_PPTX))
    print(f"Successfully generated exact presentation: {OUTPUT_PPTX}")
    print(f"Slide count: {len(prs.slides)}")


if __name__ == "__main__":
    build_presentation()
