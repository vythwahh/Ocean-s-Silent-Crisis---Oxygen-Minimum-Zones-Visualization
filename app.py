import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import streamlit as st
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# ── Page config ──────────────────────────────────────────
st.set_page_config(page_title="OMZ Dashboard", layout="wide")

st.title("🌊 Oxygen Minimum Zones Dashboard")
st.markdown("**Data:** Copernicus Marine Service — Global Ocean BGC Reanalysis | 2022-11-30")

# ── Load data ────────────────────────────────────────────
@st.cache_data
def load_data():
    return xr.open_dataset(
        "/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen /cmems_mod_glo_bgc_my_0.25deg_P1D-m_1742228470209.nc",
        engine="h5netcdf"
    )

ds = load_data()
depths = [float(d) for d in ds.depth.values]

# ── Sidebar ──────────────────────────────────────────────
st.sidebar.header("⚙️ Controls")
selected_depth = st.sidebar.select_slider(
    "Select depth (m)",
    options=[f"{d:.0f}" for d in depths],
    value=f"{depths[3]:.0f}"
)
depth_idx = [f"{d:.0f}" for d in depths].index(selected_depth)

omz_threshold = st.sidebar.slider("OMZ threshold (mmol/m³)", 20, 120, 60, step=5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🦈 Why it matters")
st.sidebar.markdown(
    st.sidebar.markdown(
    "Oxygen Minimum Zones are regions where O₂ drops below **60 mmol/m³**. "
    "Marine organisms are forced into thin oxygenated surface layers, "
    "disrupting feeding, reproduction, and migration across entire ecosystems."
)
)

# ── Row 1: Map ───────────────────────────────────────────
st.subheader(f"🗺️ Dissolved Oxygen Map — Depth: {selected_depth}m")

o2_slice = ds["o2"].isel(time=0, depth=depth_idx)

fig1, ax1 = plt.subplots(
    figsize=(14, 6),
    subplot_kw={"projection": ccrs.PlateCarree()}
)
img = ax1.contourf(
    ds.longitude, ds.latitude, o2_slice,
    levels=30, cmap="RdYlBu", vmin=0, vmax=380,
    transform=ccrs.PlateCarree()
)
ax1.contour(
    ds.longitude, ds.latitude, o2_slice,
    levels=[omz_threshold], colors="black",
    linewidths=1.5, linestyles="--",
    transform=ccrs.PlateCarree()
)
ax1.add_feature(cfeature.LAND, facecolor="#d4c9a8", zorder=1)
ax1.add_feature(cfeature.COASTLINE, linewidth=0.6, zorder=2)
ax1.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5, zorder=2)
ax1.gridlines(draw_labels=True, linewidth=0.4, alpha=0.5, linestyle="--")
plt.colorbar(img, ax=ax1, label="O₂ (mmol/m³)", shrink=0.85)
ax1.set_title(f"Depth: {selected_depth}m | OMZ boundary: {omz_threshold} mmol/m³", fontsize=13)
st.pyplot(fig1)
plt.close(fig1)

# ── Row 2: Depth profile + Stats ─────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📉 Depth Profile — 3 Regions")
    points = {
        "Eastern Pacific (OMZ)": {"lat": 10.0,  "lon": 250.0, "color": "#D32F2F"},
        "Central Pacific":       {"lat": 0.0,   "lon": 180.0, "color": "#F57C00"},
        "Southern Ocean":        {"lat": -60.0, "lon": 200.0, "color": "#1565C0"},
    }
    fig2, ax2 = plt.subplots(figsize=(6, 7))
    for label, pt in points.items():
        profile = ds["o2"].isel(time=0).sel(
            latitude=pt["lat"], longitude=pt["lon"], method="nearest"
        )
        ax2.plot(profile.values, depths, color=pt["color"],
                 linewidth=2.5, label=label, marker="o", markersize=4)
    ax2.axvline(x=omz_threshold, color="black", linestyle="--",
                linewidth=1.5, label=f"Threshold ({omz_threshold})")
    ax2.invert_yaxis()
    ax2.set_xlabel("O₂ (mmol/m³)")
    ax2.set_ylabel("Depth (m)")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)
    st.pyplot(fig2)
    plt.close(fig2)

with col2:
    st.subheader("📊 Stats at selected depth")
    o2_vals = o2_slice.values.flatten()
    o2_vals = o2_vals[~np.isnan(o2_vals)]

    omz_pct = (o2_vals < omz_threshold).sum() / len(o2_vals) * 100

    m1, m2, m3 = st.columns(3)
    m1.metric("Mean O₂", f"{o2_vals.mean():.1f}", "mmol/m³")
    m2.metric("Min O₂",  f"{o2_vals.min():.1f}",  "mmol/m³")
    m3.metric("OMZ area", f"{omz_pct:.1f}%", "of ocean")

    st.markdown("---")
    st.markdown("### 🌡️ O₂ Distribution")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.hist(o2_vals, bins=50, color="#1565C0", alpha=0.7, edgecolor="white")
    ax3.axvline(x=omz_threshold, color="red", linestyle="--",
                linewidth=2, label=f"OMZ threshold ({omz_threshold})")
    ax3.set_xlabel("O₂ (mmol/m³)")
    ax3.set_ylabel("Count")
    ax3.legend()
    ax3.grid(alpha=0.3)
    st.pyplot(fig3)
    plt.close(fig3)

st.markdown("---")
st.caption("Data: Copernicus Marine Service (CMEMS) · Global Ocean BGC Reanalysis · Mercator Ocean")