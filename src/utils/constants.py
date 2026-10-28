"""
==================================================
Project Constants
==================================================
"""

# Hazard Categories

HAZARD_LEVELS = {

    (0.00, 0.20): "Very Low",

    (0.21, 0.40): "Low",

    (0.41, 0.60): "Moderate",

    (0.61, 0.80): "High",

    (0.81, 1.00): "Very High"

}

# Earth Radius

EARTH_RADIUS = 6371000

# Gravity

GRAVITY = 9.81

# Water Density

WATER_DENSITY = 1025

# NDWI Threshold

NDWI_THRESHOLD = 0.0

# Default CRS

CRS = "EPSG:4326"

# Missing Data

NODATA = -9999