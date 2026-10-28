"""
DEM Loader

Loads a Digital Elevation Model (DEM) from a GeoTIFF file.
"""

from pathlib import Path

from .raster_loader import RasterLoader


class DEMLoader(RasterLoader):

    def __init__(self, data_dir=None):

        super().__init__(data_dir)

    # --------------------------------------------------

    def download(self):

        raise NotImplementedError(
            "DEM files should be downloaded manually."
        )

    # --------------------------------------------------

    def load(self, filename):

        return self.read_raster(filename)

    # --------------------------------------------------

    def preprocess(self, filename):

        raster = self.load(filename)

        self.validate(raster)

        return raster

    # --------------------------------------------------

    def validate(self, raster):

        if raster["data"] is None:

            raise ValueError(
                "DEM raster is empty."
            )

        if raster["crs"] is None:

            raise ValueError(
                "DEM CRS is missing."
            )

        return True