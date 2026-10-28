"""
Dataset URLs

All download links are stored here.
"""

from config import RAW_DATA


class DatasetURLs:

    # USGS API

    USGS_EVENT = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
    )

    # These will be filled in later with the
    # exact URLs for Palu DEM and GEBCO.

    DEM = None

    GEBCO = None

    ALTIMETRY = None


class DatasetPaths:

    EARTHQUAKE = RAW_DATA / "earthquake"

    DEM = RAW_DATA / "dem"

    BATHYMETRY = RAW_DATA / "bathymetry"

    SENTINEL1 = RAW_DATA / "sentinel1"

    SENTINEL2 = RAW_DATA / "sentinel2"

    ALTIMETRY = RAW_DATA / "altimetry"