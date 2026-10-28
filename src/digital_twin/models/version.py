"""
version.py

Version information for the Digital Twin.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class VersionInfo:

    number: int = 1

    created_at: datetime = datetime.utcnow()

    author: str = "Digital Twin Engine"

    description: str = ""

    def bump(self):

        self.number += 1

        self.created_at = datetime.utcnow()