import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

os.chdir("/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen ")
ds = xr.open_dataset("/Users/vythu/Documents/Copernicus Marine Dataviz Challenge/Dissolved Oxygen /cmems_mod_glo_bgc_my_0.25deg_P1D-m_1742228470209.nc", engine="h5netcdf")

configs = {
    "cartopy_221m_final": {"idx": 0,  "depth": "221m", "omz": "6.8%"},
    "cartopy_458m_final": {"idx": 7,  "depth": "458m", "omz": "15.5%"},
    "cartopy_947m_final": {"idx": 14, "depth": "947m", "omz": "27.8%"},
}

ocean_labels = [
    (200, 40,  "NORTH PACIFIC OCEAN"),
    (200, -40, "SOUTH PACIFIC OCEAN"),
    (310, 20,  "ATLANTIC\nOCEAN"),
    (160, -55, "SOUTHERN OCEAN"),
    (115, 20,  "INDIAN\nOCEAN"),
]

for fname, cfg in configs.items():
    o2 = ds["o2"].isel(time=0, depth=cfg["idx"])

    fig, ax = plt.subplots(figsize=(12, 5),
                           subplot_kw={"projection": ccrs.PlateCarree()})
    img = ax.contourf(
        ds.longitude, ds.latitude, o2,
        levels=30, cmap="RdYlBu", vmin=0, vmax=380,
        transform=ccrs.PlateCarree()
    )
    ax.contour(
        ds.longitude, ds.latitude, o2,
        levels=[60], colors="black", linewidths=1.3, linestyles="--",
        transform=ccrs.PlateCarree()
    )
    ax.add_feature(cfeature.LAND, facecolor="#d4c9a8", zorder=1)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=2)
    ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4, linestyle="--")

    for lon, lat, name in ocean_labels:
        ax.text(lon, lat, name,
            transform=ccrs.PlateCarree(),
            fontsize=7.5, color="white", alpha=1.0,
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
    cbar.set_label("O₂ (mmol/m³)", fontsize=9)
    cbar.ax.text(1.6, 0.02, "← No oxygen\n   (dead zone)",
                 transform=cbar.ax.transAxes,
                 fontsize=7.5, color="#D32F2F", va="bottom")
    cbar.ax.text(1.6, 0.95, "← Healthy\n   oxygen",
                 transform=cbar.ax.transAxes,
                 fontsize=7.5, color="#1565C0", va="top")

    red_patch  = mpatches.Patch(color="#D32F2F", label="No oxygen — marine life cannot survive")
    blue_patch = mpatches.Patch(color="#4FC3F7", label="Healthy oxygen levels")
    line_patch = plt.Line2D([0], [0], color="black", lw=1.3,
                             linestyle="--", label="Critical boundary (60 mmol/m³)")
    ax.legend(handles=[red_patch, blue_patch, line_patch],
              loc="lower left", fontsize=8, framealpha=0.9)

    ax.set_title(
        f"Depth: {cfg['depth']}  |  {cfg['omz']} of ocean below survival threshold  |  2022-11-30",
        fontsize=11, fontweight="bold"
    )

    plt.tight_layout()
    plt.savefig(f"{fname}.png", dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {fname}.png")