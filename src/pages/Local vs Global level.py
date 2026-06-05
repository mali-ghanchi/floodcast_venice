import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.title("🌊 Global vs Local Sea Level — Venice vs Global Mean")

st.markdown("""
This page compares **global mean sea level (GMSL)** from satellite altimetry
with **local relative sea level in Venice** from the tide gauge.

- **Global Mean Sea Level (GMSL)** reflects large–scale climate processes  
  (thermal expansion, glacier and ice-sheet melt).
- **Venice tide gauge** measures **relative sea level**, which additionally
  includes **land subsidence** and local/regional ocean dynamics.
""")

# ===================================
# 1. LOAD LOCAL (VENICE) SEA LEVEL
# ===================================

sea = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
sea.columns = ['year', 'sea_level_mm', 'flag', 'quality']
sea = sea[sea['sea_level_mm'] != -99999]
sea['sea_level_cm'] = sea['sea_level_mm'] / 10
sea = sea[['year', 'sea_level_cm']]

# ===================================
# 2. LOAD GLOBAL MEAN SEA LEVEL (NASA)
# ===================================

# NASA_SSH_GMSL_INDICATOR.txt: high-frequency GMSL (approx. 10-day/weekly)
# We skip header lines starting with "HDR" (comment='H') and split on whitespace.
gmsl_raw = pd.read_csv(
    'data/NASA_SSH_GMSL_INDICATOR.txt',
    sep=r"\s+",
    engine="python",
    comment='H',
    header=None
)

# col 0 = decimal year (e.g. 1993.01), col 1 = GMSL (cm), col 2 = smoothed GMSL (cm)
gmsl_raw.columns = ['year_decimal', 'gmsl_cm', 'gmsl_cm_smooth']

# Extract calendar year (integer)
gmsl_raw['year'] = gmsl_raw['year_decimal'].astype(int)

# Annual mean of smoothed GMSL (cm)
gmsl_annual = (
    gmsl_raw
    .groupby('year', as_index=False)[['gmsl_cm_smooth']]
    .mean()
    .rename(columns={'gmsl_cm_smooth': 'gmsl_cm'})
)

# ===================================
# 3. MERGE GLOBAL & LOCAL (OVERLAP PERIOD)
# ===================================

df_merged = sea.merge(gmsl_annual, on='year', how='inner')

if df_merged.empty:
    st.error("No overlapping years between Venice tide gauge and NASA GMSL dataset.")
    st.stop()

year_min = int(df_merged['year'].min())
year_max = int(df_merged['year'].max())

st.markdown(f"**Overlap period:** {year_min}–{year_max}")

# ===================================
# 4. CREATE ANOMALIES (RELATIVE TO 1993)
# ===================================

# Choose a reference year for anomalies (1993 is natural for GMSL)
ref_year = 1993
if ref_year not in df_merged['year'].values:
    # If 1993 not present in overlap, fall back to first overlap year
    ref_year = int(df_merged['year'].min())

row_ref = df_merged[df_merged['year'] == ref_year].iloc[0]

# Local Venice anomaly (cm above ref_year level)
df_merged['venice_anom_cm'] = df_merged['sea_level_cm'] - row_ref['sea_level_cm']

# Global anomaly (NASA is around 1993 mean, we re-center exactly to ref_year)
df_merged['gmsl_anom_cm'] = df_merged['gmsl_cm'] - row_ref['gmsl_cm']

# Difference: local minus global (approx. subsidence + regional effects)
df_merged['local_minus_global_cm'] = df_merged['venice_anom_cm'] - df_merged['gmsl_anom_cm']

# ===================================
# 5. PLOT: GLOBAL vs LOCAL ANOMALIES
# ===================================

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_merged['year'],
    y=df_merged['venice_anom_cm'],
    name='Venice Relative Sea Level (Anomaly)',
    mode='lines',
    line=dict(color='steelblue', width=2)
))

fig.add_trace(go.Scatter(
    x=df_merged['year'],
    y=df_merged['gmsl_anom_cm'],
    name='Global Mean Sea Level (Anomaly)',
    mode='lines',
    line=dict(color='black', width=2, dash='dash')
))

fig.update_layout(
    title=f'Global vs Local Sea Level — Anomalies relative to {ref_year}',
    xaxis_title='Year',
    yaxis_title='Sea Level Anomaly (cm)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# ===================================
# 6. PLOT: LOCAL MINUS GLOBAL (SUBSIDENCE SIGNAL)
# ===================================

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_merged['year'],
    y=df_merged['local_minus_global_cm'],
    name='Venice – Global Mean Sea Level',
    mode='lines',
    line=dict(color='darkred', width=2)
))

fig2.update_layout(
    title='Local Amplification: Venice Relative Sea Level minus Global Mean',
    xaxis_title='Year',
    yaxis_title='Local minus Global (cm)',
    hovermode='x unified'
)

st.plotly_chart(fig2, use_container_width=True)

# ===================================
# 7. INTERPRETATION
# ===================================

st.markdown(f"""
### Interpretation

The **global GMSL curve** (dashed black) shows how the **average ocean level**
has changed globally since about {ref_year}, mainly due to:

- thermal expansion of warming oceans,  
- melting glaciers and ice sheets,  
- changes in land water storage.

The **Venice curve** (blue) shows how the **relative sea level** at the tide gauge
has evolved over the same period. Because this is measured relative to the land,
it includes not only global sea-level rise, but also:

- **land subsidence** (the city and lagoon sinking),  
- regional ocean and lagoon dynamics.

The lower plot (**Venice – Global**) highlights the **local amplification** of
sea-level rise:

- If this difference increases over time, Venice is rising **faster** than the
  global mean, which is consistent with **ongoing subsidence** and local effects.
- This means that even if global mean sea level rises by a certain amount,
  the **effective relative sea level** experienced in Venice can be higher,
  bringing **flood thresholds and Acqua Alta events forward in time**.

For planners and civil protection, this comparison emphasizes that:

- Global climate scenarios (RCPs) provide the **baseline** rise,  
- but **local subsidence** and regional processes are crucial for assessing the
  true **flood risk in Venice**, and cannot be ignored when designing defenses,
  infrastructure upgrades, or evacuation strategies.
""")