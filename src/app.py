import streamlit as st

st.set_page_config(
    page_title="FloodCast Venice",
    layout="wide"
)

# -------------------------
# TITLE
# -------------------------
st.title("FloodCast Venice - Water you thinking? 💦")

st.subheader(
    "About the city"
)

# -------------------------
# INTRODUCTION
# -------------------------
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
# IMAGES
# -------------------------
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

# -------------------------
# NAVIGATION SECTION
# -------------------------
st.markdown("---")

st.header("📊 Explore the Analysis")

col1, col2, col3 = st.columns(3)

# -------------------------
# HISTORICAL ANALYSIS
# -------------------------
with col1:

    st.subheader("📈 Historical Analysis")

    st.write("""
    Explore historical tide gauge measurements and
    regression-based future predictions.
    """)

    st.page_link(
        "pages/historical_analysis.py",
        label="Open Historical Analysis",
        icon="📈"
    )

# -------------------------
# CLIMATE SCENARIOS
# -------------------------
with col2:

    st.subheader("🌍 Climate Scenarios")

    st.write("""
    Analyse future sea level rise under
    different RCP climate pathways.
    """)

    st.page_link(
        "pages/climate_scenarios.py",
        label="Open Climate Scenarios",
        icon="🌍"
    )

# -------------------------
# COMPARISON DASHBOARD
# -------------------------
with col3:

    st.subheader("⚖️ Comparative Dashboard")

    st.write("""
    Compare historical trends, regression predictions,
    and climate scenarios side-by-side.
    """)

    st.page_link(
        "pages/comparison_dashboard.py",
        label="Open Comparative Dashboard",
        icon="⚖️"
    )