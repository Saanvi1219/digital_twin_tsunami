"""
==========================================================
Digital Twin Tsunami Prediction System

Study Area :
2018 Sulawesi (Palu) Earthquake & Tsunami

Author :
==========================================================
"""

from pathlib import Path

# -------------------------------
# PROJECT PATHS
# -------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA = DATA_DIR / "raw"

PROCESSED_DATA = DATA_DIR / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

LOG_DIR = PROJECT_ROOT / "logs"

MODEL_DIR = PROJECT_ROOT / "models"

ASSET_DIR = PROJECT_ROOT / "assets"

# -------------------------------
# STUDY AREA
# -------------------------------

# ==========================================================
# STUDY EVENT
# ==========================================================

STUDY_EVENT = {

    "name": "Sulawesi_2018",

    "country": "Indonesia",

    "city": "Palu",

    "latitude": -0.178,

    "longitude": 119.840,

    "start_date": "2018-09-28",

    "end_date": "2018-09-29",

    "min_magnitude": 7.4,

    "max_magnitude": 7.6,

    "radius_km": 250

}

# -------------------------------
# FILES
# -------------------------------

NDWI_PRE = RAW_DATA / "sentinel2" / "NDWI_pre.tiff"

NDWI_POST = RAW_DATA / "sentinel2" / "NDWI_post.tiff"

NDWI_DIFF = RAW_DATA / "sentinel2" / "NDWI_diff.tif"

FLOOD_MASK = RAW_DATA / "sentinel2" / "Flood_mask.tif"

DEM_FILE = RAW_DATA / "dem" / "SRTM_DEM.tif"

BATHYMETRY_FILE = RAW_DATA / "bathymetry" / "GEBCO.tif"

# -------------------------------
# DTII WEIGHTS
# -------------------------------

ALPHA = 0.20
BETA = 0.20
GAMMA = 0.15
DELTA = 0.15
LAMBDA = 0.20
MU = 0.10

# -------------------------------
# OUTPUTS
# -------------------------------

HAZARD_MAP = OUTPUT_DIR / "maps" / "hazard_map.png"

DTII_MAP = OUTPUT_DIR / "maps" / "dtii_map.png"

VALIDATION_REPORT = OUTPUT_DIR / "validation" / "metrics.csv"