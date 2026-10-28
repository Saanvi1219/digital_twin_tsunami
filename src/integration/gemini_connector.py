"""
gemini_connector.py

Connects the Adaptive Digital Twin
to Gemini for AI-powered analysis.
"""

from src.gemini.gemini_client import GeminiClient


class GeminiConnector:

    def __init__(self):

        self.client = GeminiClient()

    # =====================================================

    def analyse(

        self,

        features,

        simulation_summary,

        dtii_result,

    ):

        prompt = f"""
You are an AI tsunami risk analyst.

Earthquake Magnitude:
{features.earthquake.magnitude}

Mean Elevation:
{features.mean_elevation:.2f}

Mean Bathymetry:
{features.mean_bathymetry:.2f}

Maximum Wave Height:
{simulation_summary["max_wave"]:.2f}

Flooded Area:
{simulation_summary["flooded_area"]:.2f} km²

Maximum Runup:
{simulation_summary["max_runup"]:.2f}

Highest Risk:
{simulation_summary["highest_risk"]:.2f}

DTII Score:
{dtii_result["score"]}

Risk Level:
{dtii_result["level"]}

Provide:

1. Tsunami Summary
2. Infrastructure Impact
3. Evacuation Recommendation
4. Risk Explanation
5. Confidence
"""

        return self.client.generate(prompt)