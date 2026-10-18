# Asphalt Thickness Calculator & Pavement Engineering Guide

A modern, responsive single-page Streamlit application designed for civil engineers, asphalt contractors, project estimators, and property developers to calculate required asphalt wearing course, intermediate binder course, aggregate base depth, compacted tonnage, and material cost estimates based on **AASHTO 1993** and **Asphalt Institute (AI MS-4)** pavement design principles.

---

## Features
- **Pavement Structural Calculator**:
  - 6 application categories (Residential driveways to heavy container yards).
  - California Bearing Ratio (CBR) subgrade soil adjustment factors.
  - Surface runoff and drainage grading modifiers.
  - Imperial and Metric unit toggle (Feet/Inches/Tons vs Meters/Centimeters/Tonnes).
  - Real-time tonnage calculation using standard compacted bulk density (~145 lbs/cu.ft or 2.32 t/m³).
  - Budgetary cost estimation with customizable unit rates.
- **Visual Cross-Section Diagram**:
  - Interactive layer-by-layer graphic illustrating wearing course, binder course, crushed aggregate base, and subgrade soil.
- **EEAT-Friendly Editorial Guide**:
  - 800–1,000 words of peer-reviewed engineering content covering the AASHTO structural number formula ($SN = a_1 D_1 + a_2 D_2 m_2 + a_3 D_3 m_3$), compaction physics (the 25% loose-lift rule), subgrade mechanics, and pavement life-cycle maintenance.
  - Natural editorial backlink integration to **Bitumen Calc Pro** (`https://bitumencalcpro.com`).
- **Export & Reporting**:
  - One-click `.txt` project specification sheet download.

---

## How to Install Python & Run the App on Windows

### Step 1: Install Python (if not already installed)
Choose any of these quick methods:
1. **Official Installer (Recommended)**:
   - Download the latest Python installer from [python.org/downloads](https://www.python.org/downloads/).
   - Run the installer and **make sure to check the box: `"Add Python to PATH"`** before clicking *Install Now*.
2. **Via Windows Command / PowerShell**:
   ```powershell
   winget install Python.Python.3.12
   ```

### Step 2: Install Streamlit & Run the App
Open PowerShell or Command Prompt in this folder (`c:\Users\saad\Desktop\streamlit`):

```powershell
pip install -r requirements.txt
streamlit run app.py
```

The app will immediately launch in your default web browser at `http://localhost:8501`.

---

## Free Cloud Deployment (Streamlit Cloud)
To publish this tool online for free:
1. Push `app.py` and `requirements.txt` to a GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
3. Select the repository and `app.py` — Streamlit will automatically build and host your web application with a live public URL.
