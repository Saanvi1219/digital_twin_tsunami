"""
==================================================
File Manager
==================================================
"""

from pathlib import Path

class FileManager:

    @staticmethod
    def ensure_directory(path):

        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def file_exists(path):

        return Path(path).exists()

    @staticmethod
    def create_directories():

        folders = [

            "data/raw",

            "data/processed",

            "outputs/maps",

            "outputs/reports",

            "outputs/validation",

            "logs",

            "models"

        ]

        for folder in folders:

            Path(folder).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def list_files(folder):

        folder = Path(folder)

        if not folder.exists():

            return []

        return list(folder.glob("*"))