
from .nodes.image_nodes import ResizeImageBatch
from .nodes.trajectory_nodes import ResizeTrajectoryBatch
NODE_CONFIG = {
    "ResizeImageBatch": {"class": ResizeImageBatch, "name": "ResizeImageBatch"},
    "ResizeTrajectoryBatch": {"class": ResizeTrajectoryBatch, "name": "ResizeTrajectoryBatch"},
}

def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__)

    return node_class_mappings, node_display_name_mappings

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
