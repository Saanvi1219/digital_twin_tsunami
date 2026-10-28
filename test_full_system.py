"""
test_full_system.py

Complete Digital Twin system diagnostic.

Checks:
1. Imports
2. Digital Twin creation
3. Earthquake loading
4. DEM loading
5. Bathymetry loading
6. Twin readiness
7. Twin validation
8. Twin state
9. Simulation engine
10. Graph agent
11. LLM agent
12. Complete orchestrator
"""

import traceback
import numpy as np


# ============================================================
# TEST RESULT HELPER
# ============================================================

def test(name, function):

    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)

    try:

        result = function()

        print(f"✓ {name}: PASSED")

        if result is not None:
            print("Result:")
            print(result)

        return True

    except Exception as e:

        print(f"✗ {name}: FAILED")
        print(f"Error: {e}")

        traceback.print_exc()

        return False


# ============================================================
# 1. DIGITAL TWIN IMPORT
# ============================================================

def test_digital_twin_import():

    from src.digital_twin.core.twin import DigitalTwin

    return DigitalTwin


# ============================================================
# 2. CREATE DIGITAL TWIN
# ============================================================

def create_twin():

    from src.digital_twin.core.twin import DigitalTwin

    twin = DigitalTwin()

    print("Twin created:")
    print(twin)

    return twin


# ============================================================
# 3. EARTHQUAKE
# ============================================================

def test_earthquake(twin):

    earthquake = {

        "event": "M 7.5 - 72 km N of Palu, Indonesia",

        "latitude": -0.2559,

        "longitude": 119.8462,

        "depth": 20.0,

        "magnitude": 7.5,

    }

    twin.load_earthquake(earthquake)

    print("Earthquake state:")
    print(twin.state.earthquake)

    return twin.state.earthquake


# ============================================================
# 4. DEM
# ============================================================

def test_dem(twin):

    dem = np.random.rand(
        256,
        256
    ).astype(np.float32)

    twin.load_dem(dem)

    print(
        "DEM shape:",
        twin.state.dem.shape
    )

    return twin.state.dem.shape


# ============================================================
# 5. BATHYMETRY
# ============================================================

def test_bathymetry(twin):

    bathymetry = np.random.rand(
        256,
        256
    ).astype(np.float32)

    twin.load_bathymetry(
        bathymetry
    )

    print(
        "Bathymetry shape:",
        twin.state.bathymetry.shape
    )

    return twin.state.bathymetry.shape


# ============================================================
# 6. TWIN READINESS
# ============================================================

def test_readiness(twin):

    ready = twin.is_ready()

    print(
        "Twin ready:",
        ready
    )

    if not ready:

        raise RuntimeError(
            "Digital Twin is NOT ready."
        )

    return ready


# ============================================================
# 7. VALIDATION
# ============================================================

def test_validation(twin):

    valid, report = twin.validate()

    print(
        "Validation:",
        valid
    )

    print(
        "Report:",
        report
    )

    return report


# ============================================================
# 8. STATE INSPECTION
# ============================================================

def test_state(twin):

    state = twin.state

    print("\nDIGITAL TWIN STATE")
    print("-" * 50)

    print(
        "Earthquake:",
        state.earthquake is not None
    )

    print(
        "DEM:",
        state.dem is not None
    )

    print(
        "Bathymetry:",
        state.bathymetry is not None
    )

    print(
        "Sentinel-1:",
        state.sentinel1 is not None
    )

    print(
        "Sentinel-2:",
        state.sentinel2 is not None
    )

    print(
        "Altimetry:",
        state.altimetry is not None
    )

    print(
        "Simulation:",
        state.simulation_result is not None
    )

    print(
        "Prediction:",
        state.prediction is not None
    )

    print(
        "Confidence:",
        state.confidence
    )

    print(
        "Version:",
        state.version
    )

    return state.to_dict()


# ============================================================
# 9. DIGITAL TWIN SUMMARY
# ============================================================

def test_summary(twin):

    summary = twin.summary()

    print(
        "Digital Twin Summary:"
    )

    print(summary)

    return summary


# ============================================================
# 10. DIGITAL TWIN HEALTH
# ============================================================

def test_health(twin):

    health = twin.health()

    print(
        "Digital Twin Health:"
    )

    print(health)

    return health


# ============================================================
# 11. GRAPH AGENT IMPORT
# ============================================================

def test_graph_import():

    from src.agents.graph_agent import GraphAgent

    return GraphAgent


# ============================================================
# 12. GRAPH AGENT
# ============================================================

def test_graph():

    from src.agents.graph_agent import GraphAgent

    graph_agent = GraphAgent()

    print(
        "Graph Agent created:"
    )

    print(graph_agent)

    return graph_agent


# ============================================================
# 13. LLM IMPORT
# ============================================================

def test_llm_import():

    from src.agents.llm_agent import LLMAgent

    return LLMAgent


# ============================================================
# 14. LLM AGENT INITIALIZATION
# ============================================================

def test_llm_initialization():

    from src.agents.llm_agent import LLMAgent

    agent = LLMAgent()

    print(
        "LLM Agent initialized:"
    )

    print(agent)

    return agent


# ============================================================
# 15. GEMINI DIRECT TEST
# ============================================================

def test_gemini_direct():

    from llm.gemini_agent import GeminiTsunamiAgent

    agent = GeminiTsunamiAgent()

    print(
        "Gemini model:",
        getattr(
            agent,
            "model",
            "unknown"
        )
    )

    return agent


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print(" ADAPTIVE TSUNAMI DIGITAL TWIN - FULL SYSTEM TEST ")
    print("=" * 70)

    results = {}

    # --------------------------------------------------------
    # IMPORTS
    # --------------------------------------------------------

    results["Digital Twin Import"] = test(
        "Digital Twin Import",
        test_digital_twin_import
    )

    # --------------------------------------------------------
    # CREATE TWIN
    # --------------------------------------------------------

    try:

        twin = create_twin()

        print(
            "\n✓ Digital Twin object created successfully."
        )

    except Exception as e:

        print(
            "\n✗ Could not create Digital Twin."
        )

        traceback.print_exc()

        return

    # --------------------------------------------------------
    # TWIN TESTS
    # --------------------------------------------------------

    results["Earthquake"] = test(
        "Earthquake Loading",
        lambda: test_earthquake(twin)
    )

    results["DEM"] = test(
        "DEM Loading",
        lambda: test_dem(twin)
    )

    results["Bathymetry"] = test(
        "Bathymetry Loading",
        lambda: test_bathymetry(twin)
    )

    results["Readiness"] = test(
        "Digital Twin Readiness",
        lambda: test_readiness(twin)
    )

    results["Validation"] = test(
        "Digital Twin Validation",
        lambda: test_validation(twin)
    )

    results["State"] = test(
        "Digital Twin State",
        lambda: test_state(twin)
    )

    results["Summary"] = test(
        "Digital Twin Summary",
        lambda: test_summary(twin)
    )

    results["Health"] = test(
        "Digital Twin Health",
        lambda: test_health(twin)
    )

    # --------------------------------------------------------
    # GRAPH
    # --------------------------------------------------------

    results["Graph Import"] = test(
        "Graph Agent Import",
        test_graph_import
    )

    results["Graph Agent"] = test(
        "Graph Agent Initialization",
        test_graph
    )

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    results["LLM Import"] = test(
        "LLM Agent Import",
        test_llm_import
    )

    results["LLM Initialization"] = test(
        "LLM Agent Initialization",
        test_llm_initialization
    )

    results["Gemini"] = test(
        "Gemini Direct Initialization",
        test_gemini_direct
    )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 70)
    print(" FINAL SYSTEM TEST REPORT ")
    print("=" * 70)

    passed = 0
    failed = 0

    for name, result in results.items():

        if result:

            print(
                f"✓ {name}"
            )

            passed += 1

        else:

            print(
                f"✗ {name}"
            )

            failed += 1

    print()
    print(
        f"PASSED : {passed}"
    )

    print(
        f"FAILED : {failed}"
    )

    print("=" * 70)

    if failed == 0:

        print(
            "✓ ALL TESTS PASSED"
        )

    else:

        print(
            "⚠ SOME TESTS FAILED"
        )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()