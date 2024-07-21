# image_utils.py
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import filters

def extract_line_art(line_art_path, smooth_factor=0.5, threshold_adj=0):
    line_art = Image.open(line_art_path).convert("L")
    line_art_array = np.array(line_art)
    thresh = filters.threshold_otsu(line_art_array)
    binary = line_art_array < (thresh - threshold_adj)
    smoothed = ndimage.gaussian_filter(binary.astype(float), sigma=smooth_factor)
    final_binary = (smoothed > 0.5).astype(np.uint8)
    result = np.zeros((line_art_array.shape[0], line_art_array.shape[1], 4), dtype=np.uint8)
    result[:,:,3] = 255 * final_binary
    result[:,:,0:3] = 255 * final_binary[:,:,np.newaxis]
    return Image.fromarray(result)

def apply_shading_with_line_art(flat_color_path, brightness_map_path, line_art_path, highlight_strength=0.5, shadow_strength=0.5):
    brightness_map = np.array(Image.open(brightness_map_path).convert('L')).astype(float)
    brightness_standardized = (brightness_map - np.mean(brightness_map)) / np.std(brightness_map)
    highlight_mask = np.clip(brightness_standardized, 0, None)
    shadow_mask = np.clip(-brightness_standardized, 0, None)
    flat_color = np.array(Image.open(flat_color_path).convert('RGBA')).astype(float)
    result = flat_color.copy()
    for i in range(3):
        result[:,:,i] = np.clip(flat_color[:,:,i] + (highlight_mask * 255 * highlight_strength), 0, 255)
    shadow_factor = 1 - (shadow_mask * shadow_strength)
    for i in range(3):
        result[:,:,i] = np.clip(result[:,:,i] * shadow_factor, 0, 255)
    line_art = extract_line_art(line_art_path)
    result_image = Image.fromarray(result.astype('uint8'))
    result_image.paste(line_art, (0, 0), line_art)
    return result_image
