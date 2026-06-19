import streamlit as st

st.set_page_config(
    page_title="FloodCast Venice",
    layout="wide"
)

# -------------------------
# TITLE + INTRO
# -------------------------
st.title("FloodCast Venice - Water you thinking? 💦")

st.subheader("About the city")

st.markdown("""
Venice is one of the most flood-prone cities in the world due to
rising sea levels, land subsidence, and climate change.

FloodCast Venice - Water you thinking? is an interactive decision-support dashboard
designed to analyse historical sea level trends and compare future
flooding risks under different climate scenarios.

We are here to raise awareness about the growing issue within Venice and intend to support urban planners,
government authorities, and civil protection agencies in
understanding long-term flood risks and infrastructure challenges. Furthermore, it could also be used by tourists, should they choose to travel.
""")

# -------------------------
# KPI CARDS (OVERVIEW)
# -------------------------
st.markdown("### Key figures at a glance")

kcol1, kcol2, kcol3, kcol4 = st.columns(4)

with kcol1:
    st.metric(label="Historical Dataset Range", value="1909–2000")

with kcol2:
    st.metric(label="Prediction Horizon", value="2100")

with kcol3:
    st.metric(label="Estimated Trend", value="+2.3 mm/year")

with kcol4:
    st.metric(label="Flood Risk Assessment", value="High")

# -------------------------
# NAVIGATION SECTION (MOVED UP)
# -------------------------
st.markdown("---")

st.header("📊 Explore the analysis")

nav1, nav2, nav3, nav4 = st.columns(4)

# HISTORICAL ANALYSIS
with nav1:
    st.subheader("📈 Historical Analysis")
    st.write("""
    Explore historical tide gauge measurements and
    a simple regression-based future trend.
    """)
    st.page_link(
        "pages/historical_analysis.py",
        label="Open Historical Analysis",
        icon="📈"
    )

# CLIMATE-DRIVEN MODEL
with nav2:
    st.subheader("🌍 Climate-Driven Model")
    st.write("""
    Use global temperature and CO₂, together with time,
    to model Venice sea level and explore extrapolated futures
    with statistical prediction intervals.
    """)
    st.page_link(
        "pages/climate_scenarios.py",
        label="Open Climate-Driven Model",
        icon="🌍"
    )

# COMPARISON DASHBOARD
with nav3:
    st.subheader("⚖️ Comparative Dashboard")
    st.write("""
    Compare our climate-driven prediction with RCP-based
    sea level scenarios to assess medium and high-end risks.
    """)
    st.page_link(
        "pages/comparison_dashboard.py",
        label="Open Comparative Dashboard",
        icon="⚖️"
    )

# GLOBAL vs LOCAL SEA LEVEL
with nav4:
    st.subheader("🌊 Global vs Local Sea Level")
    st.write("""
    Contrast Venice tide gauge data with global mean sea level
    to highlight local land subsidence and regional amplification.
    """)
    st.page_link(
        "pages/Local vs Global level.py",
        label="Open Global vs Local View",
        icon="🌊"
    )

# -------------------------
# GLIMPSE + IMAGES SECTION (LOWER)
# -------------------------
st.markdown("---")

st.markdown("### A glimpse into a sinking city")

st.markdown("""
These images show how recurrent flooding and relative sea-level rise
affect daily life in Venice, from emergency response to tourism and heritage sites.
""")

# Fundraiser link (placeholder URL – replace with real one)
st.markdown(
    """
    [👉 Support flood relief and adaptation efforts in Venice](https://www.savevenice.org/project/immediate-response-fund)
    """,
    unsafe_allow_html=False
)

# IMAGES
col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "assets/venice flood.jpg",
        caption="Flooding in Venice"
    )

with col2:
    st.image(
        "assets/venice.jpg",
        caption="Venice Grand Canal"
    )

with col3:
    st.image(
        "assets/aqua alta.jpg",
        caption="Acqua Alta"
    )