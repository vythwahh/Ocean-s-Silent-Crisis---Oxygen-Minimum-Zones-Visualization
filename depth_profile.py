import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

ds = xr.open_dataset("/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen /cmems_mod_glo_bgc_my_0.25deg_P1D-m_1742228470209.nc", engine="h5netcdf")

 
points = {
    "Eastern Pacific (OMZ severe)": {"lat": 10.0,  "lon": 250.0},
    "Central Pacific (moderate)":   {"lat": 0.0,   "lon": 180.0},
    "Southern Ocean (healthy)":     {"lat": -60.0, "lon": 200.0},
}

fig, ax = plt.subplots(figsize=(8, 10))

colors = ["#D32F2F", "#F57C00", "#1565C0"]

for (label, pt), color in zip(points.items(), colors):
    profile = ds["o2"].isel(time=0).sel(
        latitude=pt["lat"], longitude=pt["lon"], method="nearest"
    )
    ax.plot(profile.values, ds.depth.values, color=color, linewidth=2.5, label=label, marker="o", markersize=5)

 
ax.axvline(x=60, color="black", linestyle="--", linewidth=1.5, label="OMZ threshold (60 mmol/m³)")

ax.invert_yaxis()
ax.set_xlabel("Dissolved Oxygen (mmol/m³)", fontsize=12)
ax.set_ylabel("Depth (m)", fontsize=12)
ax.set_title("Oxygen Depth Profile — 3 Ocean Regions\n2022-11-30", fontsize=14)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.set_facecolor("#f8f9fa")
fig.patch.set_facecolor("#ffffff")

plt.tight_layout()
plt.savefig("depth_profile.png", dpi=150)
plt.show()
print("Saved: depth_profile.png")