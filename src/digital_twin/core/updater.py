from __future__ import annotations

from typing import Any, Dict

from src.digital_twin.core.state_manager import StateManager


class TwinUpdater:
    """
    High-level state updater.

    Handles all state modifications.
    """

    def __init__(self, manager: StateManager):

        self.manager = manager
            # --------------------------------------------------

    def update_earthquake(
        self,
        earthquake: Dict[str, Any]
    ):

        """
        Update earthquake information.
        """

        self.manager.update(

            earthquake=earthquake

        )
            # --------------------------------------------------

    def update_dem(
        self,
        dem
    ):

        """
        Update DEM.
        """

        self.manager.update(

            dem=dem

        )
            # --------------------------------------------------

    def update_bathymetry(
        self,
        bathymetry
    ):

        self.manager.update(

            bathymetry=bathymetry

        )
            # --------------------------------------------------

    def update_sentinel1(
        self,
        image
    ):

        self.manager.update(

            sentinel1=image

        )

    # --------------------------------------------------

    def update_sentinel2(
        self,
        image
    ):

        self.manager.update(

            sentinel2=image

        )
            # --------------------------------------------------

    def update_simulation(
        self,
        tsunami=None,
        inundation=None,
        hazard_map=None,
        evacuation_map=None
    ):

        self.manager.update(

            tsunami=tsunami,

            inundation=inundation,

            hazard_map=hazard_map,

            evacuation_map=evacuation_map

        )
            # --------------------------------------------------

    def update_prediction(
        self,
        prediction,
        confidence
    ):

        self.manager.update(

            prediction=prediction,

            confidence=confidence

        )
            # --------------------------------------------------

    def update_metadata(
        self,
        **kwargs
    ):

        for key, value in kwargs.items():

            self.manager.set_metadata(

                key,

                value

            )
                # --------------------------------------------------

    def update(
        self,
        **kwargs
    ):

        """
        Generic update interface.

        Example
        -------

        updater.update(
            earthquake=data,
            dem=dem
        )
        """

        self.manager.update(

            **kwargs

        )
            # --------------------------------------------------

    def clear_predictions(self):

        self.manager.clear_predictions()

    # --------------------------------------------------

    def reset_simulation(self):

        self.manager.reset_simulation()

    # --------------------------------------------------

    def reset(self):

        self.manager.reset()
            # --------------------------------------------------

    @property
    def state(self):

        return self.manager.state

    # --------------------------------------------------

    def summary(self):

        return self.manager.summary()

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"TwinUpdater("

            f"version={self.state.version})"

        )
        