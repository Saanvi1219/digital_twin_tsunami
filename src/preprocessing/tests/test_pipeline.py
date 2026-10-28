from src.preprocessing.pipeline import PreprocessingPipeline

pipeline = PreprocessingPipeline()

datasets = pipeline.run(

    earthquake_file="us2000ahv0",

    dem_file="raw/dem/DEM.tif",

    bathymetry_file="raw/bathymetry/bathymetry.tif",

    sentinel1_file="raw/sentinel1/sentinel1.tif",

    sentinel2_file="raw/sentinel2/sentinel2.tif",

    altimetry_file="raw/altimetry/altimetry.csv",

)

print()

print(datasets.keys())