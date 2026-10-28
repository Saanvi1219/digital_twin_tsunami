"""
version_control.py

Manages versioning of the Digital Twin.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from src.digital_twin.models.version import VersionInfo


class VersionController:
    """
    Centralized version manager.

    Responsible for:

    • Creating versions
    • Version lookup
    • Tags
    • Metadata
    • History
    """

    def __init__(self):

        self._current = VersionInfo()

        self._history: List[VersionInfo] = []

        self._tags: Dict[str, int] = {}

        self.commit(
            description="Initial Version"
        )
            # --------------------------------------------------

    def commit(
        self,
        description: str = "",
        author: str = "Digital Twin Engine"
    ) -> VersionInfo:
        """
        Create a new version.
        """

        version = VersionInfo(

            number=self._current.number,

            created_at=datetime.utcnow(),

            author=author,

            description=description

        )

        self._history.append(version)

        self._current.bump()

        return version
        # --------------------------------------------------

    @property
    def current(self):

        return self._history[-1]

    # --------------------------------------------------

    @property
    def next_number(self):

        return self._current.number
        # --------------------------------------------------

    def get(
        self,
        version: int
    ) -> VersionInfo:

        for v in self._history:

            if v.number == version:

                return v

        raise ValueError(

            f"Version {version} not found."

        )
            # --------------------------------------------------

    def tag(
        self,
        tag: str,
        version: Optional[int] = None
    ):

        if version is None:

            version = self.current.number

        self._tags[tag] = version

    # --------------------------------------------------

    def get_tag(
        self,
        tag: str
    ) -> VersionInfo:

        version = self._tags[tag]

        return self.get(version)
        # --------------------------------------------------

    def search(
        self,
        keyword: str
    ):

        results = []

        keyword = keyword.lower()

        for version in self._history:

            if keyword in version.description.lower():

                results.append(version)

        return results
        # --------------------------------------------------

    def timeline(self):

        return [

            {

                "version": v.number,

                "author": v.author,

                "description":

                    v.description,

                "created_at":

                    v.created_at.isoformat()

            }

            for v in self._history

        ]
            # --------------------------------------------------

    @property
    def total_versions(self):

        return len(self._history)

    # --------------------------------------------------

    @property
    def latest(self):

        return self.current

    # --------------------------------------------------

    def versions(self):

        return [

            version.number

            for version in self._history

        ]
            # --------------------------------------------------

    def export(self):

        return {

            "total_versions":

                self.total_versions,

            "versions":

                self.timeline(),

            "tags":

                self._tags

        }
            # --------------------------------------------------

    def clear(self):

        self._history.clear()

        self._tags.clear()

        self._current = VersionInfo()

    # --------------------------------------------------

    def __len__(self):

        return len(self._history)

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"VersionController("

            f"versions={len(self)})"

        )
        