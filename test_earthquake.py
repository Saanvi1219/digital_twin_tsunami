from src.preprocessing.loaders import EarthquakeLoader

loader = EarthquakeLoader()

earthquake = loader.load()

print()

print("=" * 50)

for key, value in earthquake.items():

    print(f"{key:<15}: {value}")

print("=" * 50) 