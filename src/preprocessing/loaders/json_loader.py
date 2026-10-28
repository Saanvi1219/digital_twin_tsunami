"""
JSON Loader

Utility class for JSON files.
"""

import json

from .base_loader import BaseLoader


class JsonLoader(BaseLoader):

    # --------------------------------------------------

    def read_json(self, filename):

        path = self.get_path(filename)

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)

    # --------------------------------------------------

    def save_json(self, data, filename):

        path = self.get_path(filename)

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4
            )

        return path