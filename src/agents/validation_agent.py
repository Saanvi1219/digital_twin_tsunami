"""
Validation Agent

Validates simulated tsunami inundation against
observed satellite-derived flood observations.

Validation includes:

1. Spatial agreement
   - F1 Score
   - IoU
   - Precision
   - Recall

2. Continuous agreement
   - RMSE
   - MAE
   - Pearson Correlation

Continuous metrics are calculated only when
a continuous observed reference is available.

A binary flood mask is NOT treated as a
continuous flood-depth measurement.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np


class ValidationAgent:

    def __init__(self, threshold: float = 0.5):

        self.threshold = threshold
        self.last_result = None

    # ==========================================================
    # ARRAY CONVERSION
    # ==========================================================

    @staticmethod
    def _array(value):

        if value is None:
            return None

        try:

            array = np.asarray(
                value,
                dtype=float
            )

            if array.size == 0:
                return None

            return array

        except Exception:

            return None

    # ==========================================================
    # ALIGN ARRAYS
    # ==========================================================

    @staticmethod
    def _align(predicted, observed):

        if predicted is None or observed is None:
            return None, None

        if predicted.shape == observed.shape:
            return predicted, observed

        if (
            predicted.ndim >= 2
            and observed.ndim >= 2
        ):

            rows = min(
                predicted.shape[-2],
                observed.shape[-2]
            )

            cols = min(
                predicted.shape[-1],
                observed.shape[-1]
            )

            predicted = predicted[
                ...,
                :rows,
                :cols
            ]

            observed = observed[
                ...,
                :rows,
                :cols
            ]

            return predicted, observed

        return None, None

    # ==========================================================
    # VALID PIXELS
    # ==========================================================

    @staticmethod
    def _valid_pixels(
        predicted,
        observed
    ):

        predicted = np.asarray(
            predicted,
            dtype=float
        )

        observed = np.asarray(
            observed,
            dtype=float
        )

        valid = (
            np.isfinite(predicted)
            &
            np.isfinite(observed)
        )

        return (
            predicted[valid],
            observed[valid]
        )

    # ==========================================================
    # RMSE
    # ==========================================================

    @staticmethod
    def rmse(
        predicted,
        observed
    ):

        predicted, observed = (
            ValidationAgent._valid_pixels(
                predicted,
                observed
            )
        )

        if len(predicted) == 0:
            return None

        error = predicted - observed

        return float(
            np.sqrt(
                np.mean(
                    error ** 2
                )
            )
        )

    # ==========================================================
    # MAE
    # ==========================================================

    @staticmethod
    def mae(
        predicted,
        observed
    ):

        predicted, observed = (
            ValidationAgent._valid_pixels(
                predicted,
                observed
            )
        )

        if len(predicted) == 0:
            return None

        error = np.abs(
            predicted - observed
        )

        return float(
            np.mean(error)
        )

    # ==========================================================
    # PRECISION
    # ==========================================================

    @staticmethod
    def precision(
        predicted_mask,
        observed_mask
    ):

        predicted_mask = (
            predicted_mask.astype(bool)
        )

        observed_mask = (
            observed_mask.astype(bool)
        )

        tp = np.logical_and(
            predicted_mask,
            observed_mask
        ).sum()

        fp = np.logical_and(
            predicted_mask,
            ~observed_mask
        ).sum()

        denominator = tp + fp

        if denominator == 0:
            return 1.0

        return float(
            tp / denominator
        )

    # ==========================================================
    # RECALL
    # ==========================================================

    @staticmethod
    def recall(
        predicted_mask,
        observed_mask
    ):

        predicted_mask = (
            predicted_mask.astype(bool)
        )

        observed_mask = (
            observed_mask.astype(bool)
        )

        tp = np.logical_and(
            predicted_mask,
            observed_mask
        ).sum()

        fn = np.logical_and(
            ~predicted_mask,
            observed_mask
        ).sum()

        denominator = tp + fn

        if denominator == 0:
            return 1.0

        return float(
            tp / denominator
        )

    # ==========================================================
    # F1 SCORE
    # ==========================================================

    @staticmethod
    def f1_score(
        predicted_mask,
        observed_mask
    ):

        precision = ValidationAgent.precision(
            predicted_mask,
            observed_mask
        )

        recall = ValidationAgent.recall(
            predicted_mask,
            observed_mask
        )

        denominator = (
            precision + recall
        )

        if denominator == 0:
            return 0.0

        return float(
            2.0
            * precision
            * recall
            / denominator
        )

    # ==========================================================
    # IOU
    # ==========================================================

    @staticmethod
    def iou(
        predicted_mask,
        observed_mask
    ):

        predicted_mask = (
            predicted_mask.astype(bool)
        )

        observed_mask = (
            observed_mask.astype(bool)
        )

        intersection = np.logical_and(
            predicted_mask,
            observed_mask
        ).sum()

        union = np.logical_or(
            predicted_mask,
            observed_mask
        ).sum()

        if union == 0:
            return 1.0

        return float(
            intersection / union
        )

    # ==========================================================
    # PEARSON CORRELATION
    # ==========================================================

    @staticmethod
    def pearson(
        predicted,
        observed
    ):

        predicted, observed = (
            ValidationAgent._valid_pixels(
                predicted,
                observed
            )
        )

        if len(predicted) < 2:
            return None

        predicted_std = np.std(
            predicted
        )

        observed_std = np.std(
            observed
        )

        if (
            predicted_std == 0
            or observed_std == 0
        ):
            return None

        correlation = np.corrcoef(
            predicted,
            observed
        )[0, 1]

        if np.isnan(correlation):
            return None

        return float(correlation)

    # ==========================================================
    # METRIC AVAILABILITY
    # ==========================================================

    @staticmethod
    def _continuous_reference(features):

        possible_fields = [
            "observed_depth",
            "observed_flood_depth",
            "reference_depth",
            "observed_wave",
            "observed_wave_height",
            "reference_wave",
            "reference_wave_height"
        ]

        for field in possible_fields:

            value = getattr(
                features,
                field,
                None
            )

            if value is not None:

                array = ValidationAgent._array(
                    value
                )

                if array is not None:
                    return array, field

        return None, None

    # ==========================================================
    # CONFUSION MATRIX
    # ==========================================================

    @staticmethod
    def confusion_matrix(
        predicted_mask,
        observed_mask
    ):

        predicted_mask = (
            predicted_mask.astype(bool)
        )

        observed_mask = (
            observed_mask.astype(bool)
        )

        tp = int(
            np.logical_and(
                predicted_mask,
                observed_mask
            ).sum()
        )

        tn = int(
            np.logical_and(
                ~predicted_mask,
                ~observed_mask
            ).sum()
        )

        fp = int(
            np.logical_and(
                predicted_mask,
                ~observed_mask
            ).sum()
        )

        fn = int(
            np.logical_and(
                ~predicted_mask,
                observed_mask
            ).sum()
        )

        return {
            "true_positive": tp,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn
        }

    # ==========================================================
    # EXECUTE
    # ==========================================================

    def execute(
        self,
        simulation_result,
        features
    ) -> Dict[str, Any]:

        print(
            "\n[VALIDATION AGENT] "
            "Validating simulation..."
        )

        # ======================================================
        # PREDICTED SIMULATION OUTPUT
        # ======================================================

        try:

            predicted_depth = self._array(
                simulation_result
                .inundation
                .flood_depth
            )

            predicted_mask = self._array(
                simulation_result
                .inundation
                .inundation_mask
            )

        except Exception as exc:

            result = {

                "valid": False,

                "reason":
                    f"Unable to extract "
                    f"simulation output: {exc}",

                "rmse": None,
                "mae": None,
                "depth_rmse": None,
                "depth_mae": None,

                "f1_score": None,
                "iou": None,
                "pearson": None,

                "precision": None,
                "recall": None,

                "confidence": 0.0,

                "prediction_quality":
                    "INVALID",

                "continuous_validation":
                    False

            }

            self.last_result = result

            return result

        # ======================================================
        # OBSERVED FLOOD MASK
        # ======================================================

        observed_mask = getattr(
            features,
            "water_mask",
            None
        )

        observed_mask = self._array(
            observed_mask
        )

        if observed_mask is None:

            result = {

                "valid": False,

                "reason":
                    "Observed flood mask unavailable.",

                "rmse": None,
                "mae": None,
                "depth_rmse": None,
                "depth_mae": None,

                "f1_score": None,
                "iou": None,
                "pearson": None,

                "precision": None,
                "recall": None,

                "confidence": 0.0,

                "prediction_quality":
                    "INVALID",

                "continuous_validation":
                    False

            }

            self.last_result = result

            print(
                "[VALIDATION AGENT] "
                "Observed flood mask unavailable."
            )

            return result

        # ======================================================
        # ALIGN PREDICTED MASK WITH OBSERVED MASK
        # ======================================================

        predicted_mask, observed_mask = (
            self._align(
                predicted_mask,
                observed_mask
            )
        )

        if (
            predicted_mask is None
            or observed_mask is None
        ):

            result = {

                "valid": False,

                "reason":
                    "Prediction and observation "
                    "could not be aligned.",

                "rmse": None,
                "mae": None,
                "depth_rmse": None,
                "depth_mae": None,

                "f1_score": None,
                "iou": None,
                "pearson": None,

                "precision": None,
                "recall": None,

                "confidence": 0.0,

                "prediction_quality":
                    "INVALID",

                "continuous_validation":
                    False

            }

            self.last_result = result

            return result
        
        
        print("\n========== VALIDATION DIAGNOSTICS ==========")
        print("Predicted mask")
        print("Shape :", predicted_mask.shape)
        print("Min   :", np.min(predicted_mask))
        print("Max   :", np.max(predicted_mask))
        print("Mean  :", np.mean(predicted_mask))
        print("Std   :", np.std(predicted_mask))
        print("Flood pixels :", np.sum(predicted_mask > self.threshold))

        print("\nObserved mask")
        print("Shape :", observed_mask.shape)
        print("Min   :", np.min(observed_mask))
        print("Max   :", np.max(observed_mask))
        print("Mean  :", np.mean(observed_mask))
        print("Std   :", np.std(observed_mask))
        print("Flood pixels :", np.sum(observed_mask > self.threshold))

        print("\nPredicted unique values:")
        print(np.unique(predicted_mask)[:20])

        print("\nObserved unique values:")
        print(np.unique(observed_mask)[:20])

        print("\n============================================")
        
        
        print("\nPredicted Flood Depth")
        print("Shape :", predicted_depth.shape)
        print("Min   :", np.min(predicted_depth))
        print("Max   :", np.max(predicted_depth))
        print("Mean  :", np.mean(predicted_depth))
        print("Std   :", np.std(predicted_depth))
        print("Values > 0.5 :", np.sum(predicted_depth > 0.5))
        print("Values <= 0.5:", np.sum(predicted_depth <= 0.5))

        # ======================================================
        # BINARY FLOOD MASKS
        # ======================================================

        predicted_binary = (
            predicted_mask
            > self.threshold
        )

        observed_binary = (
            observed_mask
            > self.threshold
        )

        # ======================================================
        # SPATIAL METRICS
        # ======================================================

        f1 = self.f1_score(
            predicted_binary,
            observed_binary
        )

        iou = self.iou(
            predicted_binary,
            observed_binary
        )

        precision = self.precision(
            predicted_binary,
            observed_binary
        )

        recall = self.recall(
            predicted_binary,
            observed_binary
        )

        # ======================================================
        # MASK RMSE
        # ======================================================

        mask_rmse = self.rmse(
            predicted_binary.astype(float),
            observed_binary.astype(float)
        )

        mask_mae = self.mae(
            predicted_binary.astype(float),
            observed_binary.astype(float)
        )

        # ======================================================
        # CONFUSION MATRIX
        # ======================================================

        confusion = self.confusion_matrix(
            predicted_binary,
            observed_binary
        )

        # ======================================================
        # CONTINUOUS REFERENCE
        # ======================================================

        continuous_reference, reference_name = (
            self._continuous_reference(
                features
            )
        )

        depth_rmse = None
        depth_mae = None
        pearson = None

        continuous_validation = False

        # ======================================================
        # CONTINUOUS VALIDATION
        # ======================================================

        if (
            predicted_depth is not None
            and continuous_reference is not None
        ):

            predicted_depth_aligned, reference_aligned = (
                self._align(
                    predicted_depth,
                    continuous_reference
                )
            )

            if (
                predicted_depth_aligned is not None
                and reference_aligned is not None
            ):

                depth_rmse = self.rmse(
                    predicted_depth_aligned,
                    reference_aligned
                )

                depth_mae = self.mae(
                    predicted_depth_aligned,
                    reference_aligned
                )

                pearson = self.pearson(
                    predicted_depth_aligned,
                    reference_aligned
                )

                continuous_validation = True

        # ======================================================
        # SPATIAL CORRELATION
        # ======================================================

        spatial_correlation = None

        predicted_spatial = (
            predicted_binary.astype(float)
        )

        observed_spatial = (
            observed_binary.astype(float)
        )

        if (
            np.std(predicted_spatial) > 0
            and np.std(observed_spatial) > 0
        ):

            spatial_correlation = self.pearson(
                predicted_spatial,
                observed_spatial
            )

        # ======================================================
        # CONFIDENCE
        # ======================================================

        confidence = (

            0.40 * f1

            +

            0.35 * iou

            +

            0.15 * precision

            +

            0.10 * recall

        )

        confidence = float(
            np.clip(
                confidence,
                0.0,
                1.0
            )
        )

        # ======================================================
        # QUALITY
        # ======================================================

        if confidence >= 0.80:

            quality = "HIGH"

        elif confidence >= 0.60:

            quality = "MEDIUM"

        else:

            quality = "LOW"

        # ======================================================
        # CONTINUOUS QUALITY INFORMATION
        # ======================================================

        if continuous_validation:

            continuous_status = (
                "AVAILABLE"
            )

        else:

            continuous_status = (
                "NOT_AVAILABLE"
            )

        # ======================================================
        # RESULT
        # ======================================================

        result = {

            "valid": True,

            "rmse":
                mask_rmse,

            "mae":
                mask_mae,

            "depth_rmse":
                depth_rmse,

            "depth_mae":
                depth_mae,

            "f1_score":
                f1,

            "iou":
                iou,

            "pearson":
                pearson,

            "spatial_pearson":
                spatial_correlation,

            "precision":
                precision,

            "recall":
                recall,

            "confidence":
                confidence,

            "prediction_quality":
                quality,

            "continuous_validation":
                continuous_validation,

            "continuous_reference":
                reference_name,

            "continuous_status":
                continuous_status,

            "confusion_matrix":
                confusion

        }

        self.last_result = result

        # ======================================================
        # LOGGING
        # ======================================================

        print(
            f"[VALIDATION AGENT] "
            f"Mask RMSE: {mask_rmse:.4f}"
        )

        print(
            f"[VALIDATION AGENT] "
            f"Mask MAE: {mask_mae:.4f}"
        )

        print(
            f"[VALIDATION AGENT] "
            f"F1: {f1:.4f}"
        )

        print(
            f"[VALIDATION AGENT] "
            f"IoU: {iou:.4f}"
        )

        print(
            f"[VALIDATION AGENT] "
            f"Precision: {precision:.4f}"
        )

        print(
            f"[VALIDATION AGENT] "
            f"Recall: {recall:.4f}"
        )

        if continuous_validation:

            if depth_rmse is not None:

                print(
                    f"[VALIDATION AGENT] "
                    f"Depth RMSE: "
                    f"{depth_rmse:.4f}"
                )

            if depth_mae is not None:

                print(
                    f"[VALIDATION AGENT] "
                    f"Depth MAE: "
                    f"{depth_mae:.4f}"
                )

            if pearson is not None:

                print(
                    f"[VALIDATION AGENT] "
                    f"Pearson: "
                    f"{pearson:.4f}"
                )

            else:

                print(
                    "[VALIDATION AGENT] "
                    "Pearson: N/A "
                    "(zero variance)"
                )

        else:

            print(
                "[VALIDATION AGENT] "
                "Pearson: N/A "
                "(continuous observed reference unavailable)"
            )

            print(
                "[VALIDATION AGENT] "
                "Depth RMSE: N/A "
                "(continuous observed reference unavailable)"
            )

        print(
            f"[VALIDATION AGENT] "
            f"Confidence: "
            f"{confidence:.4f}"
        )

        print(
            f"[VALIDATION AGENT] "
            f"Quality: {quality}"
        )

        print(
            "[VALIDATION AGENT] "
            f"Continuous validation: "
            f"{continuous_status}"
        )

        return result

    # ==========================================================
    # LAST RESULT
    # ==========================================================

    def last(self):

        return self.last_result