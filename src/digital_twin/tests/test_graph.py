from src.digital_twin.graph_builder import GraphBuilder
from src.digital_twin.graph_visualizer import GraphVisualizer


builder = GraphBuilder()

graph = builder.build(
    magnitude=8.2,
    deformation=1.4,
    elevation=22,
    bathymetry=4200,
    wave_height=7.1,
    inundation=65,
    prediction=0.91,
    dtii_score=0.87,
    risk_level="HIGH"
)

visualizer = GraphVisualizer(graph)

visualizer.show()

visualizer.save("digital_twin.png")