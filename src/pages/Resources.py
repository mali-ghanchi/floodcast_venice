# -----------------------------
# RESOURCES: DATA DOWNLOADS
# -----------------------------
import streamlit as st
import pandas as pd  # ensure pandas is imported

st.markdown("---")
st.markdown("## 📁 Resources – Download the data")

# Load datasets
venice_res = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
venice_res.columns = ['year', 'sea_level_mm', 'flag', 'quality']
venice_res = venice_res[venice_res['sea_level_mm'] != -99999]
venice_res['sea_level_cm'] = venice_res['sea_level_mm'] / 10

temp_res_raw = pd.read_csv('data/GLB.Ts+dSST.csv', header=None, sep=',')
temp_res = temp_res_raw[[0, 13]].copy()
temp_res.columns = ['year', 'temp_anomaly']

co2_res_raw = pd.read_csv('data/co2_annmean_mlo.csv', header=None, sep=',')
co2_res = co2_res_raw[[0, 1]].copy()
co2_res.columns = ['year', 'co2_ppm']

gmsl_res = pd.read_csv(
    'data/NASA_SSH_GMSL_INDICATOR.txt',
    sep=r"\s+",
    engine="python",
    comment='H',
    header=None
)
gmsl_res.columns = ['year_decimal', 'gmsl_cm', 'gmsl_cm_smooth']

rcp_res = pd.read_excel('data/venice_sea_level comparison.xlsx')

# 2 columns layout for buttons
col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown("**Venice tide gauge data**")
    st.download_button(
        label="Download Venice data (CSV)",
        data=venice_res.to_csv(index=False).encode('utf-8'),
        file_name="venice_tide_gauge_clean.csv",
        mime="text/csv"
    )

    st.markdown("**Global temperature anomalies (NASA GISTEMP)**")
    st.download_button(
        label="Download temperature data (CSV)",
        data=temp_res.to_csv(index=False).encode('utf-8'),
        file_name="global_temperature_anomaly.csv",
        mime="text/csv"
    )

with col_r2:
    st.markdown("**Atmospheric CO₂ (Mauna Loa)**")
    st.download_button(
        label="Download CO₂ data (CSV)",
        data=co2_res.to_csv(index=False).encode('utf-8'),
        file_name="co2_mauna_loa.csv",
        mime="text/csv"
    )

    st.markdown("**Scenario / RCP sea level data for Venice**")
    st.download_button(
        label="Download scenario data (CSV)",
        data=rcp_res.to_csv(index=False).encode('utf-8'),
        file_name="venice_scenarios.csv",
        mime="text/csv"
    )

    st.markdown("**Global Mean Sea Level (satellite altimetry)**")
    st.download_button(
        label="Download GMSL data (CSV)",
        data=gmsl_res.to_csv(index=False).encode('utf-8'),
        file_name="global_mean_sea_level_satellite.csv",
        mime="text/csv"
    )