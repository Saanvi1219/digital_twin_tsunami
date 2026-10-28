"""
Common GeoTIFF loading utilities.
"""

import rasterio
from .base_loader import BaseLoader


class RasterLoader(BaseLoader):

    def read_raster(self, filename):
        path = self.get_path(filename)

        with rasterio.open(path) as src:
            data = src.read(1)

            return {
                "data": data,
                "profile": src.profile.copy(),
                "transform": src.transform,
                "crs": src.crs,
                "bounds": src.bounds,
                "resolution": src.res,
                "width": src.width,
                "height": src.height,
                "nodata": src.nodata,
                "dtype": src.dtypes[0],
            }