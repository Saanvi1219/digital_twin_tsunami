from src.preprocessing.loaders import Sentinel1Loader

print("=" * 60)
print("SENTINEL-1 LOADER TEST")
print("=" * 60)

loader = Sentinel1Loader()

filename = "raw/sentinel1/sentinel1.tif"

image = loader.preprocess(filename)

print()

print("Rows      :", image["data"].shape[0])
print("Columns   :", image["data"].shape[1])
print("CRS       :", image["crs"])

print()

print("✓ Sentinel-1 Loader Working")