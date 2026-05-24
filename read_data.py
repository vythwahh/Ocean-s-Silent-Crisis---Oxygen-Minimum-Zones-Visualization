import xarray as xr
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors 
ds = xr.open_dataset("/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen /cmems_mod_glo_bgc_my_0.25deg_P1D-m_1742228470209.nc")

o2_slice = ds["o2"].isel(time = 0, depth = 3)
fig, ax = plt.subplots(figsize = (14,7))

img = ax.contourf(
    ds.longitude, ds.latitude, o2_slice,
    levels = 30,
    cmap="RdYlBu"
)

ax.contour(
    ds.longitude, ds.latitude, o2_slice,
    levels =[60],
    colors = "black",
    linewidths = 1.5,
    linestyles = "--"
)
cbar = plt.colorbar(img, ax = ax, label = "Dissolved Oxygen (mmol/m³)")
ax.set_title(f"Oxygen Minimum Zones — Depth: {float(ds.depth[3]):.0f}m | 2022-11-30", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("omz_map.png", dpi=150)
plt.show()
print("Saved: omz_map.png")