"""
Base Loader

Every preprocessing loader should inherit from this class.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseLoader(ABC):
    """
    Abstract base class for all preprocessing loaders.

    Handles paths safely so that paths such as:

        data/raw/dem/SRTM_DEM.tif

    are not incorrectly converted into:

        data/data/raw/dem/SRTM_DEM.tif
    """

    def __init__(self, data_dir=None):

        if data_dir is None:
            data_dir = Path.cwd() / "data"

        self.data_dir = Path(data_dir)

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # DOWNLOAD
    # ======================================================

    @abstractmethod
    def download(self):
        """
        Download raw data.

        Returns
        -------
        Path
            Location of downloaded file.
        """
        pass

    # ======================================================
    # LOAD
    # ======================================================

    @abstractmethod
    def load(self, filename):
        """
        Load dataset.

        Returns
        -------
        object
        """
        pass

    # ======================================================
    # PREPROCESS
    # ======================================================

    @abstractmethod
    def preprocess(self, filename):
        """
        Preprocess dataset.

        Returns
        -------
        object
        """
        pass

    # ======================================================
    # EXISTS
    # ======================================================

    def exists(self, filename):

        path = self.get_path(filename)

        return path.exists()

    # ======================================================
    # GET PATH
    # ======================================================

    def get_path(self, filename):
        """
        Resolve dataset path safely.

        Supported inputs:

        1. Absolute path
           C:/project/data/raw/dem/SRTM_DEM.tif

        2. Project-relative path
           data/raw/dem/SRTM_DEM.tif

        3. Filename relative to data_dir
           raw/dem/SRTM_DEM.tif
        """

        if filename is None:

            raise ValueError(
                "Filename cannot be None."
            )

        path = Path(filename)

        # --------------------------------------------------
        # Absolute path
        # --------------------------------------------------

        if path.is_absolute():

            return path

        # --------------------------------------------------
        # Already project-relative
        #
        # Example:
        # data/raw/dem/SRTM_DEM.tif
        #
        # Do NOT prepend self.data_dir again.
        # --------------------------------------------------

        if path.parts and path.parts[0].lower() == "data":

            return Path.cwd() / path

        # --------------------------------------------------
        # Relative to configured data directory
        # --------------------------------------------------

        return self.data_dir / path

    # ======================================================
    # REPRESENTATION
    # ======================================================

    def __repr__(self):

        return (
            f"{self.__class__.__name__}"
            f"(data_dir='{self.data_dir}')"
        )