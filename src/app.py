import streamlit as st

st.set_page_config(
    page_title="FloodCast Venice",
    layout="wide"
)

# -------------------------
# TITLE
# -------------------------
st.title("🌊 FloodCast Venice - Water you thinking?")

st.subheader(
    "Interactive Sea Level Prediction & Climate Risk Dashboard"
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

This application aim to raise awareness about the growing issue within Venice and is intended to support urban planners,
government authorities, and civil protection agencies in
understanding long-term flood risks and infrastructure challenges. Furthermore, it could also be used by tourists, should they choose to travel.
""")

# -------------------------
# IMAGES
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/6/6f/Venice_flood.jpg",
        caption="Flooding in Venice"
    )

with col2:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/0/0d/Venice_Grand_Canal.jpg",
        caption="Venice Grand Canal"
    )

with col3:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/a/a4/Venice_acqua_alta.jpg",
        caption="Acqua Alta Events"
    )

# -------------------------
# NAVIGATION SECTION
# -------------------------
st.markdown("---")

st.header("📊 Explore the Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### Historical Analysis

    Explore historical tide gauge measurements and
    regression-based future predictions.
    """)

with col2:
    st.warning("""
    ### Climate Scenarios

    Analyse future sea level rise under
    different RCP climate pathways.
    """)

with col3:
    st.success("""
    ### Comparative Dashboard

    Compare historical trends, regression predictions,
    and climate scenarios side-by-side.
    """)

st.markdown("""
Use the sidebar on the left to navigate between pages.
""")