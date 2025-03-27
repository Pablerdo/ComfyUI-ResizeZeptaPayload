import sys
import os

import cv2
from PIL import Image, ImageOps
# import folder_paths
import torch
import numpy as np
from io import BytesIO
import base64
import json



class ResizeTrajectories:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_width": ("INT", {"default": 1024}),
                "input_height": ("INT", {"forceInput": True}),
                "output_width": ("INT", {"default": 1024}),
                "output_height": ("INT", {"default": 1024}),
                "trajectories": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("trajectories",)
    FUNCTION = "run"
    CATEGORY = "ResizeZeptaPayload"
    DESCRIPTION = """
    Resize a batch of trajectories
    """
    def run(self, trajectories, input_width, input_height, output_width, output_height):
        # load the trajectories
        trajectories = json.loads(trajectories)
        
        # Calculate scaling factors
        scale_x = output_width / input_width
        scale_y = output_height / input_height
        
        # Process array of trajectories, where each trajectory is an array of points
        scaled_trajectories = []
        for trajectory in trajectories:
            scaled_trajectory = []
            for point in trajectory:
                # Scale x and y coordinates
                scaled_x = int(point["x"] * scale_x)
                scaled_y = int(point["y"] * scale_y)
                scaled_trajectory.append({"x": scaled_x, "y": scaled_y})
            scaled_trajectories.append(scaled_trajectory)
        
        # Convert back to JSON string
        scaled_trajectories_json = json.dumps(scaled_trajectories)
        
        return (scaled_trajectories_json,)
