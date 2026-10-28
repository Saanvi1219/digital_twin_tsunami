"""
Bathymetry Loader

Loads bathymetry GeoTIFF data.
"""

from .raster_loader import RasterLoader


class BathymetryLoader(RasterLoader):

    def __init__(self, data_dir=None):

        super().__init__(data_dir)

    # --------------------------------------------------

    def download(self):

        raise NotImplementedError(
            "Bathymetry download will be added later."
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
                "Bathymetry raster is empty."
            )

        if raster["crs"] is None:

            raise ValueError(
                "Bathymetry CRS missing."
            )

        return True