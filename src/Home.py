import streamlit as st

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="FloodCast Venice - Water you thinking? 💦",
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

FloodCast Venice - Water you thinking? 💦 is an interactive decision-support dashboard
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
# NAVIGATION SECTION
# -------------------------
st.markdown("---")
st.header("📊 Explore the analysis")

# First row: 3 cards
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
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

with row1_col2:
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

with row1_col3:
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

# Second row: 3 cards
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.subheader("🆓 Free Forecast")
    st.write("""
    Explore a standalone future sea-level forecast for Venice
    and compare the projected trend with NASA scenario data.
    """)
    st.page_link(
        "pages/free_forecast.py",
        label="Open Free Forecast",
        icon="🆓"
    )

with row2_col2:
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

with row2_col3:
    st.subheader("📁 Resources & Data")
    st.write("""
    Download the datasets used in this dashboard
    for transparency and further analysis.
    """)
    st.page_link(
        "pages/Resources.py",
        label="Open Resources",
        icon="📁"
    )

# -------------------------
# GLIMPSE + IMAGES SECTION
# -------------------------
st.markdown("---")

st.markdown("### A glimpse into a sinking city")

st.markdown("""
These images show how recurrent flooding and relative sea-level rise
affect daily life in Venice, from emergency response to tourism and heritage sites.
""")


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