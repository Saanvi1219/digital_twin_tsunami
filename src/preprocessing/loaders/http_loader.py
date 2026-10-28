"""
HTTP Loader

Reusable base class for downloading data from APIs.
"""

from pathlib import Path
import requests

from .base_loader import BaseLoader


class HttpLoader(BaseLoader):

    def __init__(self, data_dir=None, timeout=60):

        super().__init__(data_dir)

        self.timeout = timeout

    # --------------------------------------------------

    def download_file(self, url, filename):

        output_path = self.get_path(filename)

        response = requests.get(
            url,
            timeout=self.timeout
        )

        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path

    # --------------------------------------------------

    def download_json(self, url):

        response = requests.get(
            url,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()