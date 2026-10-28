"""
serializer.py

Serialization utilities for the Digital Twin.

Supports:

• JSON
• Pickle
• Automatic checkpoint creation
• State recovery
"""

from __future__ import annotations

import json
import pickle

from pathlib import Path
from datetime import datetime
from typing import Union

from src.digital_twin.models.dt_state import TwinState
from src.digital_twin.exceptions import SerializationError


class TwinSerializer:
    """
    Handles saving and loading Digital Twin states.
    """

    def __init__(self):

        self.last_saved = None
            # --------------------------------------------------

    def save_json(
        self,
        state: TwinState,
        file_path: Union[str, Path]
    ) -> Path:

        path = Path(file_path)

        try:

            with open(path, "w", encoding="utf8") as f:

                json.dump(
                    state.to_dict(),
                    f,
                    indent=4,
                    default=str
                )

            self.last_saved = datetime.utcnow()

            return path

        except Exception as e:

            raise SerializationError(str(e))
            # --------------------------------------------------

    def load_json(
        self,
        file_path: Union[str, Path]
    ) -> dict:

        path = Path(file_path)

        try:

            with open(path, "r", encoding="utf8") as f:

                return json.load(f)

        except Exception as e:

            raise SerializationError(str(e))
            # --------------------------------------------------

    def save_pickle(
        self,
        state: TwinState,
        file_path: Union[str, Path]
    ) -> Path:

        path = Path(file_path)

        try:

            with open(path, "wb") as f:

                pickle.dump(state, f)

            self.last_saved = datetime.utcnow()

            return path

        except Exception as e:

            raise SerializationError(str(e))
            # --------------------------------------------------

    def load_pickle(
        self,
        file_path: Union[str, Path]
    ) -> TwinState:

        path = Path(file_path)

        try:

            with open(path, "rb") as f:

                return pickle.load(f)

        except Exception as e:

            raise SerializationError(str(e))
            # --------------------------------------------------

    def checkpoint(
        self,
        state: TwinState,
        directory: Union[str, Path]
    ) -> Path:

        directory = Path(directory)

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (

            "checkpoint_"

            + datetime.utcnow().strftime(

                "%Y%m%d_%H%M%S"

            )

            + ".pkl"

        )

        return self.save_pickle(

            state,

            directory / filename

        )
            # --------------------------------------------------

    def export_summary(
        self,
        state: TwinState
    ) -> dict:

        return {

            "version": state.version,

            "timestamp":

                state.timestamp.isoformat(),

            "project":

                state.project,

            "scenario":

                state.scenario,

            "author":

                state.author,

            "ready":

                state.is_ready

        }
            # --------------------------------------------------

    def file_exists(

        self,

        file_path

    ):

        return Path(file_path).exists()

    # --------------------------------------------------

    def delete(

        self,

        file_path

    ):

        path = Path(file_path)

        if path.exists():

            path.unlink()

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"TwinSerializer("

            f"last_saved={self.last_saved})"

        )
        