"""
Sentinel-2 Loader

Loads Sentinel-2 optical imagery from GeoTIFF files.
"""

from .raster_loader import RasterLoader


class Sentinel2Loader(RasterLoader):

    def __init__(self, data_dir=None):

        super().__init__(data_dir)

    # --------------------------------------------------

    def download(self):

        raise NotImplementedError(
            "Automatic Sentinel-2 download will be implemented later."
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

            raise ValueError("Sentinel-2 raster is empty.")

        if raster["crs"] is None:

            raise ValueError("CRS missing.")

        return True