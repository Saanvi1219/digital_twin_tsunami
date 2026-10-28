"""
Main Entry Point

Adaptive Multi-Agent Digital Twin
for Tsunami Prediction
"""

from pathlib import Path

from src.utils.logger import get_logger
from src.agents.orchestrator_agent import OrchestratorAgent


# ==========================================================
# Logger
# ==========================================================

logger = get_logger()


# ==========================================================
# Create Project Folders
# ==========================================================

folders = [
    "outputs",
    "outputs/maps",
    "outputs/reports",
    "outputs/validation",
    "logs",
    "data/raw",
    "data/processed",
]

for folder in folders:
    Path(folder).mkdir(
        parents=True,
        exist_ok=True,
    )

logger.info("Project Initialized Successfully")


# ==========================================================
# Main
# ==========================================================

def main():

    logger.info(
        "Starting Adaptive Tsunami Digital Twin..."
    )

    # ------------------------------------------------------
    # Input Files
    # ------------------------------------------------------

    earthquake = "data/raw/earthquake/palu_2018.geojson"
    dem = "data/raw/dem/DEM.tif"
    bathymetry = "data/raw/bathymetry/bathymetry.tif"
    sentinel1 = None
    sentinel2 = "data/raw/sentinel2"
    altimetry = None

    # ------------------------------------------------------
    # Orchestrator Agent
    # ------------------------------------------------------

    orchestrator = OrchestratorAgent()

    # ------------------------------------------------------
    # Execute Pipeline
    # ------------------------------------------------------

    results = orchestrator.execute(

        earthquake,

        dem,

        bathymetry,

        sentinel1,

        sentinel2,

        altimetry,

    )

    # ------------------------------------------------------
    # Print Summary
    # ------------------------------------------------------

    logger.success(
        "Pipeline Executed Successfully"
    )

    print("\n")

    print("=" * 60)

    print(
        " ADAPTIVE MULTI-AGENT TSUNAMI DIGITAL TWIN "
    )

    print("=" * 60)

    print()

    # ------------------------------------------------------
    # Observation
    # ------------------------------------------------------

    print("Observation")

    print(
        results["observation"]
    )

    print()

    # ------------------------------------------------------
    # Simulation
    # ------------------------------------------------------

    print("Simulation Summary")

    print(
        results["summary"]
    )

    print()

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    print("Validation")

    print(
        results["validation"]
    )

    print()

    # ------------------------------------------------------
    # DTII
    # ------------------------------------------------------

    print(
        "DTII Score :",
        results["dtii"]["score"]
    )

    print()

    # ------------------------------------------------------
    # Risk
    # ------------------------------------------------------

    print(
        "Risk Score :",
        results["risk"]["risk_score"]
    )

    print()

    print(
        "Risk Level :",
        results["risk"]["risk_level"]
    )

    print()

    print(
        "Risk Priority :",
        results["risk"]["priority"]
    )

    print()
    
    # ------------------------------------------------------
# LLM ANALYSIS
# ------------------------------------------------------

    print("LLM Decision Intelligence")
    print(
        results["llm"]
    )
    print()

    # ------------------------------------------------------
    # Adaptive Decision
    # ------------------------------------------------------

    print("Adaptive Decision")

    print(
        "Adaptation Required :",
        results["adaptation"]["adaptation_required"]
    )

    print()

    print(
        "Simulation Rerun :",
        results["execution"]["simulation_rerun"]
    )

    print()

    # ------------------------------------------------------
    # Digital Twin Health
    # ------------------------------------------------------

    print("Digital Twin Health")

    print(
        results["health"]
    )

    print()

    print("=" * 60)

    logger.success(
        "Execution Complete"
    )


# ==========================================================
# Program Entry
# ==========================================================

if __name__ == "__main__":

    main()