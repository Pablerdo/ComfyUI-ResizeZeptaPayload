# Maximum resolution allowed for image operations
MAX_RESOLUTION = 8192

class ResizeImageBatch:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"forceInput": True}),
                "output_width": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "output_height": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "upscale_method": (s.upscale_methods, {"default": "bilinear"}),
                "keep_proportion": ("BOOLEAN", {"default": False}),
                "divisible_by": ("INT", {"default": 1, "min": 1, "max": 512, "step": 1}),
                "crop": (["disabled", "center"], {"default": "disabled"}),
            },
            "optional": {
                "width_input": ("INT", {"forceInput": True}),
                "height_input": ("INT", {"forceInput": True}),
                "get_size_from_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT",)
    RETURN_NAMES = ("images", "width", "height",)
    FUNCTION = "run"
    CATEGORY = "ResizeZeptaPayload"
    DESCRIPTION = """
Resizes a batch of images to the specified width and height.
Size can be retrieved from the inputs, in this order of importance:
- get_size_from_image
- width_input and height_input
- output_width and output_height widgets

Keep proportions maintains the aspect ratio of the images.
"""

    def run(self, images, output_width, output_height, upscale_method, keep_proportion, divisible_by, crop, 
           width_input=None, height_input=None, get_size_from_image=None):
        import torch
        from comfy.utils import common_upscale
        
        B, H, W, C = images.shape
        
        # Determine dimensions from inputs
        if width_input is not None:
            output_width = width_input
        if height_input is not None:
            output_height = height_input
        if get_size_from_image is not None:
            _, get_h, get_w, _ = get_size_from_image.shape
            output_height = get_h
            output_width = get_w
        
        if keep_proportion and get_size_from_image is None:
            # Scale based on which dimension is smaller in proportion to the desired dimensions
            if output_width != 0 and output_height != 0:
                ratio = min(output_width / W, output_height / H)
                output_width = round(W * ratio)
                output_height = round(H * ratio)
            # If one dimension is zero, calculate it based on ratio
            elif output_width == 0 and output_height != 0:
                ratio = output_height / H
                output_width = round(W * ratio)
            elif output_height == 0 and output_width != 0:
                ratio = output_width / W
                output_height = round(H * ratio)
        else:
            # Use original dimensions if any dimension is set to 0
            if output_width == 0:
                output_width = W
            if output_height == 0:
                output_height = H
        
        # Make dimensions divisible by the specified value
        if divisible_by > 1 and get_size_from_image is None:
            output_width = output_width - (output_width % divisible_by)
            output_height = output_height - (output_height % divisible_by)
        
        # Move channels for upscaling
        images = images.movedim(-1, 1)
        
        # Apply resize operation
        resized_images = common_upscale(images, output_width, output_height, upscale_method, crop)
        
        # Move channels back
        resized_images = resized_images.movedim(1, -1)
        
        return (resized_images, output_width, output_height,)
