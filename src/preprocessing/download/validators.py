"""
Dataset Validation Utilities
"""

from pathlib import Path


class DatasetValidator:

    @staticmethod
    def exists(file_path: Path):

        return file_path.exists()

    @staticmethod
    def not_empty(file_path: Path):

        if not file_path.exists():

            return False

        return file_path.stat().st_size > 0