# Project Plan

## Author
- Muhammad Ali Ghanchi

## Project Title
FloodCast Venice — Sea Level Rise Predictor

## Project Goal
Develop a Python-based web application that analyses historical tide gauge data from Venice, applies a linear regression model to predict future sea levels, and compares predictions against established RCP climate scenarios. The app serves as a decision-support tool for urban planners and civil protection agencies.

## Development Phases

### Phase 1 — Setup & Data Acquisition 
- Set up Python virtual environment
- Initialize Git repository and connect to GitLab
- Download historical tide gauge data from PSMSL (1909–2000)
- Download RCP projection data from Zenodo (2007–2100)
- Create project folder structure (src/, data/)

### Phase 2 — Data Processing 
- Load and clean historical tide gauge data (handle missing -99999 values)
- Convert sea level units from mm to cm
- Load and prepare RCP scenario data from Excel file
- Interpolate the 2000–2007 gap between the two datasets

### Phase 3 — Model Development 
- Train linear regression model on historical data (1909–2000)
- Extend predictions to 2100
- Add uncertainty band to predictions
- Validate model by comparing predictions against known 2000–2025 values

### Phase 4 — Visualization
- Plot historical data, trend line, prediction, and uncertainty band
- Add RCP 2.6 and RCP 8.5 scenario lines for comparison
- Convert matplotlib graphs to Plotly for interactivity

### Phase 5 — Web Application (NiceGUI/Streamlit)
- Build web app layout with title, description, and chart
- Add toggle buttons for showing/hiding individual lines (historical, RCP 2.6, RCP 8.5, prediction)
- Add flooding threshold input — user sets a cm value and app shows when it will be crossed
- Ensure app runs locally via localhost

### Phase 6 — Documentation & Submission
- Complete README.md with setup and usage instructions
- Update requirements.txt with all dependencies
- Final GitLab push with clean commit history
- Prepare 5-slide presentation


## Expected Outcome
A fully functional, web-based Python application that:
- Visualizes Venice sea level trends from 1909 to 2100
- Displays the user's own linear regression prediction alongside RCP climate scenarios
- Allows users to interactively toggle between different scenarios
- Identifies when critical flooding thresholds will be crossed
