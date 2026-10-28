from src.preprocessing.loaders import EarthquakeLoader

print("=" * 60)
print("EARTHQUAKE LOADER TEST")
print("=" * 60)

loader = EarthquakeLoader()

event = loader.preprocess(
    "us7000dflf"
)

print()

for key, value in event.items():

    print(f"{key:15}: {value}")

print()

print("✓ Earthquake Loader Working")