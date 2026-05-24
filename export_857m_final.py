import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

os.chdir("/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen ")
ds = xr.open_dataset("/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen /cmems_mod_glo_bgc_my_0.25deg_P1D-m_1742228470209.nc", engine="h5netcdf")

o2 = ds["o2"].isel(time=0, depth=13)  # 857m

fig, ax = plt.subplots(figsize=(14, 6), subplot_kw={"projection": ccrs.PlateCarree()})

img = ax.contourf(
    ds.longitude, ds.latitude, o2,
    levels=30, cmap="RdYlBu", vmin=0, vmax=380,
    transform=ccrs.PlateCarree()
)
ax.contour(
    ds.longitude, ds.latitude, o2,
    levels=[60], colors="black", linewidths=1.5, linestyles="--",
    transform=ccrs.PlateCarree()
)
ax.add_feature(cfeature.LAND, facecolor="#d4c9a8", zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.6, zorder=2)
ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4, linestyle="--")

 
ocean_labels = [
    (200, 40,  "NORTH PACIFIC OCEAN"),
    (200, -40, "SOUTH PACIFIC OCEAN"),
    (310, 20,  "ATLANTIC\nOCEAN"),
    (160, -55, "SOUTHERN OCEAN"),
    (115, 20,  "INDIAN\nOCEAN"),
]
for lon, lat, name in ocean_labels:
    ax.text(lon, lat, name,
        transform=ccrs.PlateCarree(),
        fontsize=9, color="white", alpha=1.0,
        ha="center", va="center", fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#0A3D6B",
            edgecolor="none",
            alpha=0.75
        )
    )

 
cbar = plt.colorbar(img, ax=ax, orientation="vertical",
                    fraction=0.02, pad=0.02, shrink=0.85)
cbar.set_label("Dissolved Oxygen (mmol/m³)", fontsize=10)
cbar.ax.text(1.6, 0.02, "← No oxygen\n   (dead zone)", transform=cbar.ax.transAxes,
             fontsize=8, color="#D32F2F", va="bottom")
cbar.ax.text(1.6, 0.95, "← Healthy\n   oxygen", transform=cbar.ax.transAxes,
             fontsize=8, color="#1565C0", va="top")

 
red_patch   = mpatches.Patch(color="#D32F2F", label="No oxygen — marine life cannot survive")
blue_patch  = mpatches.Patch(color="#4FC3F7", label="Healthy oxygen levels")
line_patch  = plt.Line2D([0], [0], color="black", lw=1.5,
                          linestyle="--", label="Critical boundary (60 mmol/m³)")
ax.legend(handles=[red_patch, blue_patch, line_patch],
          loc="lower left", fontsize=9, framealpha=0.9)

ax.set_title("Dissolved Oxygen at 857m — The Most Critical Depth | 2022-11-30",
             fontsize=13, fontweight="bold")

plt.tight_layout()
plt.savefig("cartopy_857m_final.png", dpi=200, bbox_inches="tight")
plt.show()
print(" Saved: cartopy_857m_final.png")