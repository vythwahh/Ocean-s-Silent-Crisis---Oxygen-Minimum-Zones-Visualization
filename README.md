# Ocean's Silent Crisis — Oxygen Minimum Zones Visualization

A data visualization project exploring how **Oxygen Minimum Zones (OMZs)** 
are expanding through the Mesopelagic Zone (200–1000m) of the Pacific Ocean, 
threatening marine ecosystems and collapsing the ocean's biological carbon pump.

Submitted to the **[Copernicus Marine Dataviz Challenge 2026](https://events.marine.copernicus.eu/ocean-sessions-dataviz-challenge)**.

---

## Key Finding

> At **857m depth**, 28% of the Pacific Ocean falls below the critical oxygen 
> threshold — the highest proportion across all measured depths. This is the 
> layer where marine organisms conduct daily vertical migrations and drive the 
> ocean's biological carbon pump.

---

## Project Structure
```
├── app.py                  # Interactive Streamlit dashboard
├── export_857m_final.py    # Hero map — most critical depth (857m)
├── export_cartopy.py       # 3 depth maps (221m, 458m, 947m)
├── depth_profile.py        # Oxygen depth profile — 3 ocean regions
├── read_data.py            # Data loading & exploration
├── cartopy_857m_final.png  # Hero map output
├── cartopy_221m_final.png  # Shallow depth map
├── cartopy_458m_final.png  # Mid depth map
├── cartopy_947m_final.png  # Deep depth map
└── chart_profile_v2.png    # Depth profile chart
---

## Stack

- **Python** — xarray, matplotlib, cartopy, numpy
- **Streamlit** — interactive dashboard
- **Data** — Copernicus Marine Service (CMEMS)
  - Product: `GLOBAL_MULTIYEAR_BGC_001_029`
  - Variable: Dissolved Oxygen (`o2`, mmol/m³)
  - Date: 30 November 2022

---

## Run the Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit dashboard
streamlit run app.py
```

---

## Data

Data is not included in this repo due to file size (~29MB).  
Download from: [Copernicus Marine Data Store](https://atlas.mercator-ocean.fr/s/SkzfKMAazqqFWdx) → folder `08 Oxygen Minimum Zones`

---

## Visualization Highlights

| Depth | OMZ Coverage | Ecosystem Impact |
|-------|-------------|-----------------|
| 221m | 6.8% | OMZ begins forming — vertical migrators still active |
| 458m | 15.5% | Dead zone doubles — migration routes disrupted |
| 857m | **28.0%** ← peak | Carbon pump severely compromised |
| 947m | 27.8% | Entire tropical Pacific below survival threshold |

---

## 📜 Data Credit

> E.U. Copernicus Marine Service Information (CMEMS)  
> Mercator Ocean International  
> Dataset: `cmems_mod_glo_bgc_my_0.25deg_P1D-m`
