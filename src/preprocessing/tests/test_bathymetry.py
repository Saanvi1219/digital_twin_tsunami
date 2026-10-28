from src.preprocessing.loaders import BathymetryLoader

print("=" * 60)
print("BATHYMETRY LOADER TEST")
print("=" * 60)

loader = BathymetryLoader()

# Adjust if your file has a different name
filename = "raw/bathymetry/bathymetry.tif"

bathy = loader.preprocess(filename)

print()

print("Rows       :", bathy["data"].shape[0])
print("Columns    :", bathy["data"].shape[1])
print("CRS        :", bathy["crs"])
print("Transform  :", bathy["transform"])

print()

print("✓ Bathymetry Loader Working")