"""
test_advanced_graphs.py

Tests the five advanced Digital Twin graphs.
"""

from src.digital_twin.advanced_graphs import (
    AdvancedGraphSuite
)


# =========================================================
# MOCK FEATURES
# =========================================================

class Earthquake:

    magnitude = 7.5


class Features:

    earthquake = Earthquake()


# =========================================================
# CURRENT PIPELINE VALUES
# =========================================================

features = Features()


simulation_summary = {

    "max_wave":
        2.238721138568347,

    "flooded_area":
        58.9824,

    "max_runup":
        2.238721138568347,

}


dtii_result = {

    "score":
        0.5001,

    "level":
        "Moderate",

    "features": {

        "seismic":
            0.7000,

        "deformation":
            0.3500,

        "elevation":
            0.8000,

        "wave":
            0.2239,

        "inundation":
            0.5898,

        "prediction":
            0.3684,

    }

}


risk_result = {

    "risk_score":
        0.2341,

    "risk_level":
        "LOW",

}


validation_result = {

    "rmse":
        0.855638,

    "depth_rmse":
        1.423794,

    "f1_score":
        0.422568,

    "iou":
        0.267883,

    "precision":
        0.267883,

    "recall":
        1.0,

    "pearson":
        0.0,

    "confidence":
        0.368446,

}


observation_result = {

    "changed":
        False,

    "anomaly":
        False,

    "change_score":
        0.0,

    "adaptation_required":
        False,

}


twin_summary = {

    "version":
        2,

    "history":
        5,

    "events":
        5,

}


# =========================================================
# GENERATE
# =========================================================

suite = AdvancedGraphSuite()

results = suite.generate_all(

    features=features,

    simulation_summary=simulation_summary,

    dtii_result=dtii_result,

    risk_result=risk_result,

    validation_result=validation_result,

    observation_result=observation_result,

    twin_summary=twin_summary,

)


print("\n" + "=" * 70)

print(
    " ADVANCED DIGITAL TWIN GRAPH TEST"
)

print("=" * 70)

for name, path in results.items():

    print(
        f"✓ {name:25} -> {path}"
    )

print("=" * 70)

print(
    "✓ ALL 5 ADVANCED GRAPHS GENERATED"
)

print("=" * 70)