from src.preprocessing.loaders import Sentinel2Loader

print("=" * 60)
print("SENTINEL-2 LOADER TEST")
print("=" * 60)

loader = Sentinel2Loader()

filename = "raw/sentinel2/sentinel2.tif"

image = loader.preprocess(filename)

print()

print("Rows      :", image["data"].shape[0])
print("Columns   :", image["data"].shape[1])
print("CRS       :", image["crs"])

print()

print("✓ Sentinel-2 Loader Working")