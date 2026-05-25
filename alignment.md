# Alignment

## Author
- Muhammad Ali Ghanchi

## Purpose
This document verifies that the FloodCast Venice project meets all requirements outlined in the AP Examination Requirements by Prof. Dr.-Ing. Tobias Miunske.

## Requirement Checklist

### 1. Definition of the Application & Business Idea ✅
- **Application:** FloodCast Venice — a sea level rise prediction and visualisation tool
- **Problem solved:** Urban planners and civil protection agencies lack a simple, accessible tool to visualise when Venice's critical flooding thresholds will be crossed
- **Business value:** Enables proactive infrastructure planning and flood risk management, reducing economic damage from unplanned flooding events
- **Target users:** Government authorities, urban planners, civil protection agencies

### 2. Data Foundation ✅
- **Historical tide gauge data:** PSMSL — Venice Punta della Salute station (1909–2000), real measured data
- **RCP projection data:** Zenodo Record 5139890 — peer-reviewed climate projections (2007–2100)
- **No synthetic data used** — both datasets are real, open-source, and from trusted scientific institutions
- **Engineering industry relevance:** Both datasets are standard references in coastal and civil engineering

### 3. Data Processing and AI Implementation ✅
- **Data cleaning:** Missing values (-99999) removed, units converted from mm to cm
- **Gap interpolation:** 2000–2007 gap between datasets handled via interpolation
- **AI model (machine learning):** Linear Regression (scikit-learn) trained on historical tide gauge data
- **Prediction:** Model forecasts sea levels from 2000 to 2100
- **Validation:** Model predictions compared against RCP scenarios for critical evaluation


## Summary
All mandatory project components are addressed. The project uses real data, applies a correctly implemented AI method, delivers a working web-based Python application, and is fully documented and version-controlled on GitLab.
