"""
Earthquake Loader

Loads earthquake information either from:

1. A local GeoJSON file
2. A USGS event ID

For the current project, the local GeoJSON file is preferred.
"""

from pathlib import Path

import json

from .base_loader import BaseLoader


class EarthquakeLoader(BaseLoader):

    # ======================================================
    # DOWNLOAD
    # ======================================================

    def download(self, event_id):

        """
        Download earthquake data from USGS.

        This is only used when a USGS event ID is supplied.
        """

        from .http_loader import HTTPJsonLoader

        url = (
            "https://earthquake.usgs.gov/"
            "fdsnws/event/1/query"
            f"?format=geojson&eventid={event_id}"
        )

        loader = HTTPJsonLoader()

        return loader.download_json(url)

    # ======================================================
    # LOAD
    # ======================================================

    def load(self, filename):

        path = self.get_path(filename)

        # --------------------------------------------------
        # Local GeoJSON
        # --------------------------------------------------

        if path.exists():

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        # --------------------------------------------------
        # Otherwise treat input as USGS event ID
        # --------------------------------------------------

        return self.download(filename)

    # ======================================================
    # PREPROCESS
    # ======================================================

    def preprocess(self, filename):

        data = self.load(filename)

        return self._extract_event(data)

    # ======================================================
    # EXTRACT EVENT
    # ======================================================

    def _extract_event(self, data):

        if not isinstance(data, dict):

            raise ValueError(
                "Invalid earthquake data."
            )

        # --------------------------------------------------
        # GeoJSON Feature
        # --------------------------------------------------

        if data.get("type") == "Feature":

            properties = data.get(
                "properties",
                {}
            )

            geometry = data.get(
                "geometry",
                {}
            )

            coordinates = geometry.get(
                "coordinates",
                []
            )

            return self._build_event(
                properties,
                coordinates
            )

        # --------------------------------------------------
        # GeoJSON FeatureCollection
        # --------------------------------------------------

        if data.get("type") == "FeatureCollection":

            features = data.get(
                "features",
                []
            )

            if not features:

                raise ValueError(
                    "Earthquake GeoJSON contains no features."
                )

            feature = features[0]

            properties = feature.get(
                "properties",
                {}
            )

            geometry = feature.get(
                "geometry",
                {}
            )

            coordinates = geometry.get(
                "coordinates",
                []
            )

            return self._build_event(
                properties,
                coordinates
            )

        # --------------------------------------------------
        # Already structured dictionary
        # --------------------------------------------------

        return {

            "event": data.get(
                "event",
                data.get(
                    "title",
                    "Unknown"
                )
            ),

            "latitude": float(
                data.get(
                    "latitude",
                    0.0
                )
            ),

            "longitude": float(
                data.get(
                    "longitude",
                    0.0
                )
            ),

            "depth": float(
                data.get(
                    "depth",
                    0.0
                )
            ),

            "magnitude": float(
                data.get(
                    "magnitude",
                    0.0
                )
            ),
        }

    # ======================================================
    # BUILD EVENT
    # ======================================================

    def _build_event(
        self,
        properties,
        coordinates
    ):

        longitude = 0.0
        latitude = 0.0
        depth = 0.0

        if len(coordinates) >= 2:

            longitude = float(
                coordinates[0]
            )

            latitude = float(
                coordinates[1]
            )

        if len(coordinates) >= 3:

            depth = float(
                coordinates[2]
            )

        # --------------------------------------------------
        # USGS depth is normally in kilometres
        # when represented in GeoJSON coordinates.
        # --------------------------------------------------

        return {

            "event": properties.get(
                "title",
                properties.get(
                    "place",
                    "Palu 2018 Earthquake"
                )
            ),

            "latitude": latitude,

            "longitude": longitude,

            "depth": depth,

            "magnitude": float(
                properties.get(
                    "mag",
                    0.0
                )
            ),

        }