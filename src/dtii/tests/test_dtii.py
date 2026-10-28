"""
test_dtii.py

Unit tests for DTII Engine.
"""

from src.dtii.dtii_engine import DTIIEngine
from src.dtii.weights import DEFAULT_WEIGHTS, validate_weights


def test_engine_creation():
    print("\nTesting DTII Engine Creation...")

    engine = DTIIEngine()

    assert engine is not None

    print("PASS: Engine Created")


def test_placeholder():
    print("\nTesting Placeholder DTII...")

    engine = DTIIEngine()

    result = engine.compute_placeholder()

    assert "score" in result
    assert "level" in result
    assert "features" in result

    print("PASS: Placeholder Computed")
    print(result)


def test_custom_features():
    print("\nTesting Custom Features...")

    engine = DTIIEngine()

    features = {

        "seismic": 0.90,

        "deformation": 0.42,

        "elevation": 0.55,

        "wave": 0.81,

        "inundation": 0.49,

        "prediction": 0.88

    }

    result = engine.compute(features)

    print(result)

    assert result["score"] > 0
    assert result["score"] <= 1

    print("PASS: Custom Features")


def test_weight_validation():

    print("\nTesting Weight Validation...")

    validate_weights(DEFAULT_WEIGHTS)

    print("PASS: Default Weights")


def test_invalid_weights():

    print("\nTesting Invalid Weights...")

    bad = {

        "seismic": 1,

        "deformation": 1,

        "elevation": 1,

        "wave": 1,

        "inundation": 1,

        "prediction": 1

    }

    try:

        validate_weights(bad)

    except ValueError:

        print("PASS: Invalid Weights Detected")

        return

    raise AssertionError("Weight validation failed")


def test_missing_feature():

    print("\nTesting Missing Feature...")

    engine = DTIIEngine()

    bad = {

        "seismic": 0.7,

        "deformation": 0.5,

        "wave": 0.8,

        "prediction": 0.9,

        "inundation": 0.3

        # elevation missing

    }

    try:

        engine.compute(bad)

    except KeyError:

        print("PASS: Missing Feature Detected")

        return

    raise AssertionError("Missing feature not detected")


def test_summary():

    print("\nTesting Summary...")

    engine = DTIIEngine()

    result = engine.compute_placeholder()

    engine.summary(result)

    print("PASS: Summary Printed")


if __name__ == "__main__":

    print("=" * 60)
    print("DTII ENGINE TEST SUITE")
    print("=" * 60)

    test_engine_creation()

    test_placeholder()

    test_custom_features()

    test_weight_validation()

    test_invalid_weights()

    test_missing_feature()

    test_summary()

    print("\n" + "=" * 60)
    print("ALL DTII TESTS PASSED")
    print("=" * 60)