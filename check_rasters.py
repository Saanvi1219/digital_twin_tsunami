import rasterio
import numpy as np

dem_path = "data/raw/dem/DEM.tif"
bathymetry_path = "data/raw/bathymetry/bathymetry.tif"

with rasterio.open(dem_path) as src:
    dem = src.read(1)

    print("========== DEM ==========")
    print("CRS:", src.crs)
    print("Resolution:", src.res)
    print("Shape:", dem.shape)
    print("Min:", np.nanmin(dem))
    print("Max:", np.nanmax(dem))
    print("Mean:", np.nanmean(dem))

with rasterio.open(bathymetry_path) as src:
    bathy = src.read(1)

    print("\n========== BATHYMETRY ==========")
    print("CRS:", src.crs)
    print("Resolution:", src.res)
    print("Shape:", bathy.shape)
    print("Min:", np.nanmin(bathy))
    print("Max:", np.nanmax(bathy))
    print("Mean:", np.nanmean(bathy))