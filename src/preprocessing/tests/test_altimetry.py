from src.preprocessing.loaders import AltimetryLoader

print("=" * 60)
print("ALTIMETRY LOADER TEST")
print("=" * 60)

loader = AltimetryLoader()

filename = "raw/altimetry/altimetry.csv"

data = loader.preprocess(filename)

print()

print(data.head())

print()

print("Rows :", len(data))

print()

print("✓ Altimetry Loader Working")