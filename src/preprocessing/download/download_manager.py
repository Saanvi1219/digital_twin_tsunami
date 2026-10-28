"""
==========================================================
Download Manager

Handles downloading and verification of datasets
for the Digital Twin Tsunami Prediction System.

Author:
==========================================================
"""

from pathlib import Path
from typing import Optional
import requests
from tqdm import tqdm

from src.utils.logger import get_logger


class DownloadManager:
    """
    Centralized Dataset Download Manager
    """

    logger = get_logger()

    @staticmethod
    def ensure_directory(directory: Path) -> None:
        """
        Create directory if it doesn't exist.
        """

        directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def file_exists(file_path: Path) -> bool:
        """
        Check if file already exists.
        """

        return file_path.exists()

    @staticmethod
    def download_file(
        url: str,
        destination: Path,
        chunk_size: int = 8192
    ) -> bool:
        """
        Generic file downloader with progress bar.
        """

        try:

            DownloadManager.ensure_directory(destination.parent)

            if destination.exists():

                DownloadManager.logger.info(
                    f"{destination.name} already exists."
                )

                return True

            response = requests.get(url, stream=True, timeout=120)

            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            DownloadManager.logger.info(
                f"Downloading {destination.name}"
            )

            with open(destination, "wb") as file:

                progress = tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True
                )

                for chunk in response.iter_content(chunk_size):

                    if chunk:

                        file.write(chunk)

                        progress.update(len(chunk))

                progress.close()

            DownloadManager.logger.success(
                f"Saved -> {destination}"
            )

            return True

        except Exception as e:

            DownloadManager.logger.error(str(e))

            return False

    @staticmethod
    def verify_file(file_path: Path) -> bool:
        """
        Verify downloaded file.
        """

        if not file_path.exists():

            return False

        if file_path.stat().st_size == 0:

            return False

        return True