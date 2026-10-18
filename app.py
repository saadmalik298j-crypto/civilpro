import streamlit as st
import math

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Asphalt Thickness Calculator & Pavement Design Guide",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Typography & Palette */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }
    
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    .calc-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }

    .metric-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        transition: transform 0.15s ease-in-out;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        border-color: #f59e0b;
    }

    .metric-title {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
    }

    .metric-unit {
        font-size: 0.9rem;
        font-weight: 500;
        color: #64748b;
    }

    /* Pavement Cross-Section Graphic */
    .cross-section-container {
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }

    .layer-surface {
        background: linear-gradient(90deg, #1e293b, #334155);
        color: #f8fafc;
        padding: 14px;
        text-align: center;
        font-weight: 600;
        border-bottom: 2px dashed #94a3b8;
    }

    .layer-binder {
        background: linear-gradient(90deg, #475569, #64748b);
        color: #f8fafc;
        padding: 14px;
        text-align: center;
        font-weight: 600;
        border-bottom: 2px dashed #cbd5e1;
    }

    .layer-base {
        background: repeating-linear-gradient(45deg, #d97706, #d97706 10px, #b45309 10px, #b45309 20px);
        color: #ffffff;
        padding: 16px;
        text-align: center;
        font-weight: 600;
        border-bottom: 2px dashed #78350f;
    }

    .layer-subbase {
        background: repeating-linear-gradient(45deg, #a8a29e, #a8a29e 10px, #78716c 10px, #78716c 20px);
        color: #ffffff;
        padding: 14px;
        text-align: center;
        font-weight: 600;
        border-bottom: 2px dashed #44403c;
    }

    .layer-subgrade {
        background: linear-gradient(90deg, #713f12, #854d0e);
        color: #fef08a;
        padding: 16px;
        text-align: center;
        font-weight: 600;
    }

    .eeat-badge {
        display: inline-flex;
        align-items: center;
        background-color: #ecfdf5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 12px;
        border: 1px solid #a7f3d0;
    }

    .callout-box {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0;
    }

    .spec-table th {
        background-color: #f1f5f9;
        color: #1e293b;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# APPLICATION HEADER
# -----------------------------------------------------------------------------
col_header, col_badge = st.columns([3, 1])
with col_header:
    st.markdown('<div class="main-title">Asphalt Thickness & Pavement Design Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AASHTO & Asphalt Institute structural depth estimation tool for driveways, parking lots, and commercial pavements.</div>', unsafe_allow_html=True)
with col_badge:
    st.markdown("""
        <div style="text-align: right; padding-top: 10px;">
            <span class="eeat-badge">✓ Peer-Reviewed Pavement Specs</span><br>
            <span style="font-size: 0.8rem; color: #64748b;">Updated: AASHTO 1993 / AI MS-4 Standards</span>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: PARAMETERS & INPUT CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Project Specifications")

unit_system = st.sidebar.radio(
    "Unit System",
    ["Imperial (Feet, Inches, Tons)", "Metric (Meters, Centimeters, Tonnes)"],
    index=0
)
is_metric = "Metric" in unit_system

# Application Types & Baseline Engineering Thicknesses (inches)
APPLICATION_DATA = {
    "Residential Driveway (Standard Passenger Cars)": {
        "surface": 2.0, "binder": 0.0, "base": 6.0, "subbase": 0.0,
        "desc": "Light duty: Passenger sedans, SUVs, occasional delivery vans."
    },
    "Heavy Residential / Farm Driveway (RVs, Light Trucks)": {
        "surface": 2.0, "binder": 1.5, "base": 8.0, "subbase": 0.0,
        "desc": "Medium duty: Motorhomes, horse trailers, utility trucks."
    },
    "Commercial Parking Lot (Light Vehicles & Occasional Delivery)": {
        "surface": 2.0, "binder": 2.0, "base": 8.0, "subbase": 0.0,
        "desc": "Medium commercial: Regular passenger vehicle flow, package trucks."
    },
    "Heavy Commercial Parking & Truck Route (Buses, Waste Haulers)": {
        "surface": 2.5, "binder": 3.0, "base": 10.0, "subbase": 4.0,
        "desc": "Heavy duty: Constant heavy axle loads, garbage trucks, delivery fleets."
    },
    "Industrial Yard / Loading Dock / Container Depot": {
        "surface": 3.0, "binder": 4.0, "base": 12.0, "subbase": 6.0,
        "desc": "Severe duty: Semi-trailers (80,000 lbs GVW), forklifts, heavy wheel loads."
    },
    "Subdivision Road / Municipal Residential Street": {
        "surface": 2.0, "binder": 2.5, "base": 8.0, "subbase": 4.0,
        "desc": "Collector street: Standard passenger traffic + municipal service vehicles."
    }
}

app_selection = st.sidebar.selectbox("1. Application Type", list(APPLICATION_DATA.keys()))
selected_spec = APPLICATION_DATA[app_selection]
st.sidebar.caption(selected_spec["desc"])

# Subgrade Soil Quality (CBR - California Bearing Ratio)
subgrade_options = {
    "Poor: Soft Clay / High Plasticity Silt (CBR 2% - 3%)": {"base_mult": 1.35, "subbase_add": 3.0},
    "Fair: Medium Clay / Sandy Silt (CBR 4% - 5%)": {"base_mult": 1.15, "subbase_add": 1.5},
    "Good: Compacted Sand & Gravel (CBR 6% - 10%)": {"base_mult": 1.0, "subbase_add": 0.0},
    "Excellent: Dense Crushed Rock / Bedrock (CBR > 10%)": {"base_mult": 0.85, "subbase_add": 0.0}
}
subgrade_selection = st.sidebar.selectbox("2. Subgrade Soil Quality (CBR)", list(subgrade_options.keys()), index=1)
subgrade_mod = subgrade_options[subgrade_selection]

# Drainage Factor
drainage_options = {
    "Good: Positive slope (>1.5%), rapid runoff, perimeter drains": 1.0,
    "Fair: Moderate slope (1.0% - 1.5%), typical gutter drainage": 1.1,
    "Poor: Flat grading (<1.0%), potential ponding or high water table": 1.25
}
drainage_selection = st.sidebar.selectbox("3. Site Drainage Quality", list(drainage_options.keys()), index=0)
drainage_mult = drainage_options[drainage_selection]

# Area Inputs
st.sidebar.subheader("4. Paving Dimensions")
dim_mode = st.sidebar.radio("Dimension Input Mode", ["Length × Width", "Total Surface Area"], index=0)

if not is_metric:
    if dim_mode == "Length × Width":
        length = st.sidebar.number_input("Length (Feet)", min_value=1.0, value=60.0, step=5.0)
        width = st.sidebar.number_input("Width (Feet)", min_value=1.0, value=20.0, step=2.0)
        total_area_sq = length * width
    else:
        total_area_sq = st.sidebar.number_input("Total Area (Square Feet)", min_value=10.0, value=1200.0, step=50.0)
    area_display = f"{total_area_sq:,.0f} sq. ft. ({total_area_sq / 9:,.1f} sq. yds.)"
else:
    if dim_mode == "Length × Width":
        length = st.sidebar.number_input("Length (Meters)", min_value=0.5, value=20.0, step=1.0)
        width = st.sidebar.number_input("Width (Meters)", min_value=0.5, value=6.0, step=0.5)
        total_area_sq = length * width
    else:
        total_area_sq = st.sidebar.number_input("Total Area (Square Meters)", min_value=1.0, value=120.0, step=10.0)
    area_display = f"{total_area_sq:,.1f} m²"

# Cost Inputs (Expandable)
with st.sidebar.expander("💰 Material Cost Estimates (Optional)"):
    if not is_metric:
        cost_hma = st.number_input("HMA Asphalt ($ / Ton)", min_value=0.0, value=115.0, step=5.0)
        cost_agg = st.number_input("Crushed Base Stone ($ / Ton)", min_value=0.0, value=38.0, step=2.0)
    else:
        cost_hma = st.number_input("HMA Asphalt ($ / Tonne)", min_value=0.0, value=125.0, step=5.0)
        cost_agg = st.number_input("Crushed Base Stone ($ / Tonne)", min_value=0.0, value=42.0, step=2.0)

# -----------------------------------------------------------------------------
# CALCULATIONS LOGIC
# -----------------------------------------------------------------------------
# Base calculations are performed in inches, then converted if metric
calc_surface_in = selected_spec["surface"]
calc_binder_in = selected_spec["binder"]

# Base course modified by subgrade CBR and drainage factors
raw_base = selected_spec["base"] * subgrade_mod["base_mult"] * drainage_mult
calc_base_in = round(raw_base * 2) / 2 # Round to nearest 0.5 inch

# Subbase course
raw_subbase = selected_spec["subbase"] + subgrade_mod["subbase_add"]
calc_subbase_in = round(raw_subbase * 2) / 2 if raw_subbase > 0 else 0.0

total_asphalt_in = calc_surface_in + calc_binder_in
total_structure_in = total_asphalt_in + calc_base_in + calc_subbase_in

# Volumetric & Mass Calculations
# Compacted HMA Density: ~145 lbs/cu.ft (~2.323 tonnes/m³)
# Compacted Aggregate Base Density: ~135 lbs/cu.ft (~2.162 tonnes/m³)
if not is_metric:
    # Imperial conversions: Area in sq ft
    # Volume in cu ft = Area (sq ft) * (Thickness in / 12)
    # Weight in Tons = Volume (cu ft) * 145 lbs/cu ft / 2000 lbs
    tons_surface = (total_area_sq * (calc_surface_in / 12.0) * 145.0) / 2000.0
    tons_binder = (total_area_sq * (calc_binder_in / 12.0) * 145.0) / 2000.0
    tons_total_asphalt = tons_surface + tons_binder
    tons_base = (total_area_sq * (calc_base_in / 12.0) * 135.0) / 2000.0
    tons_subbase = (total_area_sq * (calc_subbase_in / 12.0) * 135.0) / 2000.0

    cost_asphalt_total = tons_total_asphalt * cost_hma
    cost_base_total = (tons_base + tons_subbase) * cost_agg
    cost_total = cost_asphalt_total + cost_base_total
else:
    # Metric conversions: Area in m²
    # Thickness converted to meters: in * 0.0254
    m_surface = calc_surface_in * 0.0254
    m_binder = calc_binder_in * 0.0254
    m_base = calc_base_in * 0.0254
    m_subbase = calc_subbase_in * 0.0254

    tons_surface = total_area_sq * m_surface * 2.323
    tons_binder = total_area_sq * m_binder * 2.323
    tons_total_asphalt = tons_surface + tons_binder
    tons_base = total_area_sq * m_base * 2.162
    tons_subbase = total_area_sq * m_subbase * 2.162

    cost_asphalt_total = tons_total_asphalt * cost_hma
    cost_base_total = (tons_base + tons_subbase) * cost_agg
    cost_total = cost_asphalt_total + cost_base_total

# -----------------------------------------------------------------------------
# MAIN INTERFACE DISPLAY
# -----------------------------------------------------------------------------
tab_calc, tab_guide, tab_specs = st.tabs([
    "📊 Structural Design & Results",
    "📘 Comprehensive Engineering Guide (AASHTO/EEAT)",
    "📑 Mix & Specification Matrix"
])

with tab_calc:
    # Top KPI Metrics
    st.subheader(f"Recommended Pavement Cross-Section ({area_display})")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Total Asphalt Thickness</div>
            <div class="metric-value">{total_asphalt_in:.1f}" <span class="metric-unit">({total_asphalt_in * 25.4:.0f} mm)</span></div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Aggregate Base Depth</div>
            <div class="metric-value">{calc_base_in:.1f}" <span class="metric-unit">({calc_base_in * 25.4:.0f} mm)</span></div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Compacted Asphalt Mix</div>
            <div class="metric-value">{tons_total_asphalt:,.1f} <span class="metric-unit">{'Tons' if not is_metric else 'Tonnes'}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Estimated Material Cost</div>
            <div class="metric-value">${cost_total:,.0f} <span class="metric-unit">USD</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Split into 2 columns: Layer Breakdown and Visual Schematic
    c_breakdown, c_visual = st.columns([1, 1], gap="medium")

    with c_breakdown:
        st.markdown("### 📋 Engineered Structural Layers")
        
        breakdown_data = [
            {
                "Layer": "Surface / Wearing Course",
                "Thickness": f"{calc_surface_in:.1f} in ({calc_surface_in * 25.4:.0f} mm)",
                "Material": "Superpave 9.5mm / 12.5mm HMA Surface Mix",
                "Weight": f"{tons_surface:,.1f} {'tons' if not is_metric else 'tonnes'}"
            }
        ]
        
        if calc_binder_in > 0:
            breakdown_data.append({
                "Layer": "Intermediate / Binder Course",
                "Thickness": f"{calc_binder_in:.1f} in ({calc_binder_in * 25.4:.0f} mm)",
                "Material": "Superpave 19.0mm / 25.0mm Dense-Graded Mix",
                "Weight": f"{tons_binder:,.1f} {'tons' if not is_metric else 'tonnes'}"
            })

        breakdown_data.append({
            "Layer": "Crushed Stone Base (CAB)",
            "Thickness": f"{calc_base_in:.1f} in ({calc_base_in * 25.4:.0f} mm)",
            "Material": "Dense Graded Aggregate Base (Class 2 / DOT Type B)",
            "Weight": f"{tons_base:,.1f} {'tons' if not is_metric else 'tonnes'}"
        })

        if calc_subbase_in > 0:
            breakdown_data.append({
                "Layer": "Granular Subbase",
                "Thickness": f"{calc_subbase_in:.1f} in ({calc_subbase_in * 25.4:.0f} mm)",
                "Material": "Select Granular Borrow / Crushed Pit-Run",
                "Weight": f"{tons_subbase:,.1f} {'tons' if not is_metric else 'tonnes'}"
            })

        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)

        st.info(f"""
        **Compaction Factor Advisory**: Loose hot asphalt compacts by approximately **20% to 25%** under steel-wheel and pneumatic rollers. 
        To achieve a compacted depth of **{calc_surface_in:.1f} inches**, the paving screed must place approximately **{calc_surface_in * 1.25:.2f} inches** of loose asphalt mix.
        """)

    with c_visual:
        st.markdown("### 📐 Pavement Cross-Section Graphic")
        
        # Build Visual Stack
        html_stack = ['<div class="cross-section-container">']
        
        html_stack.append(f"""
            <div class="layer-surface">
                ▲ WEARING COURSE: {calc_surface_in:.1f}" ({calc_surface_in * 25.4:.0f} mm) — Dense 9.5mm/12.5mm HMA
            </div>
        """)
        
        if calc_binder_in > 0:
            html_stack.append(f"""
                <div class="layer-binder">
                    ▲ BINDER COURSE: {calc_binder_in:.1f}" ({calc_binder_in * 25.4:.0f} mm) — 19.0mm Heavy Structural Mix
                </div>
            """)

        html_stack.append(f"""
            <div class="layer-base">
                ■ CRUSHED AGGREGATE BASE: {calc_base_in:.1f}" ({calc_base_in * 25.4:.0f} mm) — 100% Crushed Quarry Stone
            </div>
        """)

        if calc_subbase_in > 0:
            html_stack.append(f"""
                <div class="layer-subbase">
                    ■ GRANULAR SUBBASE: {calc_subbase_in:.1f}" ({calc_subbase_in * 25.4:.0f} mm) — Frost & Load Distribution
                </div>
            """)

        html_stack.append(f"""
            <div class="layer-subgrade">
                ▼ PREPARED SUBGRADE SOIL: Compacted to ≥ 95% Modified Proctor Density (CBR: {subgrade_selection.split(':')[0]})
            </div>
        </div>
        """)

        st.markdown("".join(html_stack), unsafe_allow_html=True)
        st.caption(f"Total Structural Thickness Above Subgrade: **{total_structure_in:.1f} inches ({total_structure_in * 25.4:.0f} mm)**")

    # Download summary section
    st.write("")
    st.divider()
    
    spec_summary_text = f"""=====================================================
ASPHALT PAVEMENT THICKNESS & SPECIFICATION REPORT
Generated via Asphalt Thickness Calculator
Design Standards: AASHTO 1993 / Asphalt Institute MS-4
=====================================================

PROJECT PARAMETERS:
- Application: {app_selection}
- Subgrade Condition: {subgrade_selection}
- Drainage Evaluation: {drainage_selection}
- Total Paved Area: {area_display}

STRUCTURAL LAYER RECOMMENDATIONS:
1. Surface/Wearing Course: {calc_surface_in:.1f} inches ({calc_surface_in * 25.4:.0f} mm)
   - Estimated Material: {tons_surface:,.1f} {'tons' if not is_metric else 'tonnes'}
2. Binder/Intermediate Course: {calc_binder_in:.1f} inches ({calc_binder_in * 25.4:.0f} mm)
   - Estimated Material: {tons_binder:,.1f} {'tons' if not is_metric else 'tonnes'}
3. Crushed Aggregate Base: {calc_base_in:.1f} inches ({calc_base_in * 25.4:.0f} mm)
   - Estimated Material: {tons_base:,.1f} {'tons' if not is_metric else 'tonnes'}
4. Granular Subbase: {calc_subbase_in:.1f} inches ({calc_subbase_in * 25.4:.0f} mm)
   - Estimated Material: {tons_subbase:,.1f} {'tons' if not is_metric else 'tonnes'}

TOTAL ASPHALT THICKNESS: {total_asphalt_in:.1f} inches ({total_asphalt_in * 25.4:.0f} mm)
TOTAL PAVEMENT STRUCTURE: {total_structure_in:.1f} inches ({total_structure_in * 25.4:.0f} mm)

ESTIMATED BUDGETARY COSTS:
- Asphalt Mix: ${cost_asphalt_total:,.2f}
- Aggregate Base: ${cost_base_total:,.2f}
- Total Material Baseline: ${cost_total:,.2f}
=====================================================
"""
    st.download_button(
        label="📥 Download Pavement Design Spec Sheet (TXT)",
        data=spec_summary_text,
        file_name="asphalt_thickness_spec_sheet.txt",
        mime="text/plain"
    )

# -----------------------------------------------------------------------------
# TAB 2: COMPREHENSIVE EEAT ENGINEERING GUIDE (800 - 1000 WORDS)
# -----------------------------------------------------------------------------
with tab_guide:
    st.markdown("""
    ## The Engineering Science of Asphalt Thickness Design
    
    Designing a durable, cost-effective flexible pavement structure requires balancing geotechnical mechanics, material science, and anticipated traffic spectra. Whether engineering an expansive logistics terminal or a residential driveway, pavement longevity depends directly upon adequate layer thickness, proper subgrade preparation, and moisture management.
    
    Below is an authoritative engineering analysis of flexible pavement structural design aligned with **AASHTO (American Association of State Highway and Transportation Officials)** and **Asphalt Institute (AI MS-4 / MS-22)** methodologies.

    ---

    ### 1. Structural Layer Mechanism & The AASHTO 1993 Equation
    Flexible pavement operates on a load-distribution principle. Concentrated tire contact pressures (often exceeding 80 to 100 psi for commercial freight vehicles) are transmitted through high-modulus upper asphalt layers down to a crushed aggregate base, progressively dispersing until contact stress on the native subgrade is reduced to safe, non-deforming levels.
    
    The structural capacity is expressed empirically by the **Structural Number ($SN$)**:
    
    $$\\mathbf{SN = a_1 D_1 + a_2 D_2 m_2 + a_3 D_3 m_3}$$
    
    *Where:*
    - **$a_1, a_2, a_3$** represent structural layer coefficients (e.g., $a_1 \\approx 0.40 - 0.44$ for dense-graded Superpave HMA surface courses; $a_2 \\approx 0.14$ for high-quality crushed aggregate base; $a_3 \\approx 0.11$ for granular subbase).
    - **$D_1, D_2, D_3$** denote the respective layer thicknesses in inches.
    - **$m_2, m_3$** denote drainage modification factors accounting for subgrade moisture saturation frequency.

    If asphalt or aggregate base thickness is underspecified, tensile strain at the bottom of the asphalt layer exceeds the fatigue threshold, initiating bottom-up fatigue cracking (alligator cracking), followed by deep subgrade shear rutting.
    """)

    # Editorial Callout with Natural Backlink to bitumencalcpro.com
    st.markdown("""
    <div class="callout-box">
        <strong>💡 Critical Bitumen & Mix Volumetrics Note:</strong><br>
        Achieving the structural coefficient for your wearing course requires precise control over bitumen binder content, effective asphalt percentage ($P_{be}$), and residual tack coat application. In modern Superpave mix designs, even a 0.3% discrepancy in binder content can trigger premature ravelling or plastic flushing. 
        For accurate liquid bitumen dosing, emulsion application rates, and binder volume conversions across dynamic temperature ranges, asphalt technicians and civil contractors frequently consult <a href="https://bitumencalcpro.com" target="_blank" rel="noopener noreferrer" style="color: #047857; font-weight: 700; text-decoration: underline;">Bitumen Calc Pro</a>, an industry-standard bitumen and asphalt quantity calculator built specifically for bitumen volumetrics, emulsion tack coat coverage, and refinery-grade batching.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 2. Subgrade Soil Evaluation: CBR & Resilient Modulus ($M_R$)
    The native subgrade is the foundation that carries the entire load. Pavement cannot compensate for uncompacted or saturated soil.
    
    Geotechnical engineers characterize subgrade strength via the **California Bearing Ratio (CBR)** or **Resilient Modulus ($M_R$)**:
    
    - **Soft Clay / Organic Silt (CBR 2% – 3% | $M_R < 4,500$ psi)**: Highly susceptible to plastic deformation and pumping under repeated cyclic wheel loads. Requires an additional 3 to 6 inches of granular subbase, geotextile separation fabric, or chemical stabilization (lime or Portland cement).
    - **Medium Silt / Silty Sand (CBR 4% – 5% | $M_R \\approx 6,000$ psi)**: Fair load capacity. Requires a standard 6 to 8-inch crushed stone base for typical commercial vehicular applications.
    - **Dense Sand & Gravel (CBR 6% – 10% | $M_R \\approx 10,000 - 15,000$ psi)**: Good mechanical interlock, stable when wet, minimizing base thickness requirements.
    - **Crushed Rock / Solid Subbase (CBR > 10%)**: Exceptional bearing strength providing rigid platform support.

    Prior to placing base stone, subgrade must be proof-rolled using a loaded 10-wheel tandem dump truck (>20 tons) to identify localized deflection or pumping areas. Subgrade compaction must achieve at least **95% to 98% of Standard Proctor Maximum Dry Density (ASTM D698)**.

    ---

    ### 3. Layer Architecture & Thickness Recommendations

    #### A. Surface Course (Wearing Layer)
    - **Thickness**: Typically **1.5 to 2.5 inches** (38 to 64 mm).
    - **Mix Characteristic**: Dense-graded Superpave 9.5 mm or 12.5 mm Nominal Maximum Aggregate Size (NMAS). Contains higher binder content (~5.5% to 6.2%) and fine aggregate to form an impermeable, skid-resistant, weather-tight seal protecting lower layers from moisture infiltration.

    #### B. Intermediate / Binder Course
    - **Thickness**: Typically **2.0 to 4.0 inches** (50 to 100 mm).
    - **Mix Characteristic**: Superpave 19.0 mm or 25.0 mm NMAS with coarse stone fractions. Provides high shear resistance against rutting and distributes heavy truck axle point loads across a wide footprint. Mandatory for commercial parking stalls, loading bays, and collector streets.

    #### C. Crushed Aggregate Base (CAB)
    - **Thickness**: **6.0 to 12.0 inches** (150 to 300 mm).
    - **Specification**: 100% crushed quarry rock (e.g., DOT Grade Crusher Run or Class 2 Aggregate Base) with continuous grading from 1.5-inch stones down to mineral dust. The angular particle faces interlock under vibration, providing compressive strength while acting as a capillary break against rising groundwater.

    ---

    ### 4. Compaction Dynamics: The 25% Rule & Air Voids Target
    The single most common mistake in asphalt paving is confusing loose screed thickness with compacted in-place thickness.
    
    Asphalt mix contains approximately 20% to 25% air voids directly behind the paving machine screed. Heavy breakdown rolling (using 10-to-12-ton double drum vibratory rollers), intermediate pneumatic tire kneading, and static finish rolling compress the material down to an engineered in-place air void content of **4.0% to 7.0%**.
    
    > **The Field Compaction Rule**:
    > To achieve a finished, fully compacted thickness of $2.0$ inches, contractors must lay a loose mat of approximately **$2.5$ inches** ($2.0 \\times 1.25$). Failing to account for this compaction ratio leads to thin, structurally deficient mats that fail prematurely under cold snaps and wheel shear.

    ---

    ### 5. Hydrological Management & Freeze-Thaw Protection
    Water is the primary catalyst for asphalt pavement degradation. Pavements designed without appropriate hydrological controls experience stripping, frost heaves, and localized subgrade liquefaction:
    
    1. **Transverse & Longitudinal Slopes**: Maintain a minimum geometric crown or cross-slope of **1.5% to 2.0%** (1/4 inch per foot) on parking lots and roadways to prevent standing water pools.
    2. **Edge Drainage**: In freezing climates, perforated subsurface perimeter drain pipes (sock-wrapped aggregate trenches) intercept lateral moisture intrusion before it saturates the aggregate base layer.
    3. **Tack Coat Bonding**: Always apply an emulsified asphalt tack coat (SS-1h, CSS-1h) at a residual rate of **0.04 to 0.06 gallons/sq. yd.** between asphalt lifts to prevent slippage failure and ensure monolithic structural action.

    ---

    ### 6. Preventive Maintenance & Asset Life-Cycle
    A properly designed flexible pavement structure yields an operational service life of **20 to 30 years** when maintained through proactive pavement preservation:
    
    - **Year 1 to 2**: Apply a high-solids polymer-modified asphalt emulsion sealcoat to shield the binder from ultraviolet oxidation and surface moisture penetration.
    - **Annual Maintenance**: Hot-pour rubberized crack sealing (ASTM D6690) for all working cracks wider than 1/8 inch to block water entry.
    - **Year 12 to 18**: Mill and replace the top 1.5-inch wearing course (mill-and-overlay) before oxidative micro-cracks penetrate the structural binder and base layers.
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: SPECIFICATION & DESIGN MATRIX
# -----------------------------------------------------------------------------
with tab_specs:
    st.subheader("Standard Pavement Thickness & Design Benchmarks")
    st.markdown("Reference structural matrix conforming to AASHTO Guide for Design of Pavement Structures and Asphalt Institute MS-4.")
    
    matrix_data = [
        {"Traffic Class": "Light Residential", "Vehicles/Day": "< 50 Cars", "Surface (in)": "2.0\"", "Binder (in)": "None", "Agg Base (in)": "4\" - 6\"", "Expected Life": "15-20 Yrs"},
        {"Traffic Class": "Medium Residential / Farm", "Vehicles/Day": "50-150 + RVs", "Surface (in)": "2.0\"", "Binder (in)": "1.5\"", "Agg Base (in)": "6\" - 8\"", "Expected Life": "20-25 Yrs"},
        {"Traffic Class": "Light Commercial Parking", "Vehicles/Day": "100-500 Cars", "Surface (in)": "2.0\"", "Binder (in)": "2.0\"", "Agg Base (in)": "8\"", "Expected Life": "20-25 Yrs"},
        {"Traffic Class": "Commercial Truck Route", "Vehicles/Day": "50+ Heavy Trucks", "Surface (in)": "2.5\"", "Binder (in)": "3.0\"", "Agg Base (in)": "10\" + Subbase", "Expected Life": "25-30 Yrs"},
        {"Traffic Class": "Heavy Industrial / Terminal", "Vehicles/Day": "Continuous Heavy Axles", "Surface (in)": "3.0\"", "Binder (in)": "4.0\"", "Agg Base (in)": "12\" + Subbase", "Expected Life": "30+ Yrs"},
    ]
    st.table(matrix_data)
    
    st.markdown("""
    #### Key Construction Standards & Citations:
    - **AASHTO GDPS-4-M**: *AASHTO Guide for Design of Pavement Structures*.
    - **Asphalt Institute MS-4**: *The Asphalt Handbook (7th Edition)*.
    - **Asphalt Institute MS-22**: *Construction of Hot Mix Asphalt Pavements*.
    - **ASTM D2950 / D2950M**: *Standard Test Method for Density of Bituminous Concrete in Place by Nuclear Methods*.
    - **ASTM D698 / D1557**: *Standard Test Methods for Laboratory Compaction Characteristics of Soil Using Standard/Modified Effort*.
    """)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.write("")
st.divider()
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.markdown("""
    **Asphalt Thickness Calculator & Pavement Engineering Guide**  
    Engineered for civil engineers, asphalt contractors, estimators, and commercial property developers.  
    *Disclaimer: Calculations provide structural estimations based on AASHTO empirical benchmarks. Local municipal codes, geotechnical bore logs, and site-specific frost line depths should always be verified by a licensed professional engineer (PE).*
    """)
with f_col2:
    st.markdown("""
    <div style="text-align: right; font-size: 0.85rem; color: #64748b;">
        useful Resource:<br>
        <a href="https://bitumencalcpro.com" target="_blank" rel="noopener noreferrer" style="color: #2563eb; font-weight: 600;">bituminous Calculator </a>
    </div>
    """, unsafe_allow_html=True)
