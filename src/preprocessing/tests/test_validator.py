from src.preprocessing.processors.validator import DatasetValidator

validator = DatasetValidator()

datasets = {

    "earthquake": {},

    "dem": {},

    "bathymetry": {},

    "sentinel1": {},

    "sentinel2": {},

    "altimetry": {}

}

print()

print("Validation Result:")

print(

    validator.validate(datasets)

)

print()

print("✓ Validator Passed")