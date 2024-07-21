# 線画を2値化するノード
import os
import comfy.utils
from image_utils import extract_line_art, apply_shading_with_line_art


class LineArtProcessing:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "line_art_path": ("STRING", {"dynamicPrompts": True}),
                "smooth_factor": ("FLOAT", {"default": 0.5}),
                "threshold_adj": ("FLOAT", {"default": 0})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"

    CATEGORY = "image_processing"

    def process(self, line_art_path, smooth_factor, threshold_adj):
        return (extract_line_art(line_art_path, smooth_factor, threshold_adj),)

def before_node_execution():
    comfy.model_management.throw_exception_if_processing_interrupted()

def interrupt_processing(value=True):
    comfy.model_management.interrupt_current_processing(value)


# 線画と着色と明るさマップから１枚に合成するノード

class ShadingWithLineArt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "flat_color_path": ("STRING", {"dynamicPrompts": True}),
                "brightness_map_path": ("STRING", {"dynamicPrompts": True}),
                "line_art_path": ("STRING", {"dynamicPrompts": True}),
                "highlight_strength": ("FLOAT", {"default": 0.5}),
                "shadow_strength": ("FLOAT", {"default": 0.5})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"

    CATEGORY = "image_processing"

    def process(self, flat_color_path, brightness_map_path, line_art_path, highlight_strength, shadow_strength):
        return (apply_shading_with_line_art(flat_color_path, brightness_map_path, line_art_path, highlight_strength, shadow_strength),)
