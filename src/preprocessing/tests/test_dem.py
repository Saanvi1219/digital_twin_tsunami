from pathlib import Path

from src.preprocessing.loaders import DEMLoader

print("=" * 60)
print("DEM LOADER TEST")
print("=" * 60)

loader = DEMLoader()

# Update this filename if yours is different
filename = "raw/dem/DEM.tif"

dem = loader.preprocess(filename)

print()

print("Rows       :", dem["data"].shape[0])
print("Columns    :", dem["data"].shape[1])
print("CRS        :", dem["crs"])
print("Transform  :", dem["transform"])

print()

print("✓ DEM Loader Working")