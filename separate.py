import numpy as np
import torch

def screen_blend(A, C):
        return 1 - (1 - A) * (1 - C)

def create_difference_image(imageA, imageB):
    # 画像をテンソル (0-1範囲に正規化)
    A_tensor = imageA.float() / 255.0
    B_tensor = imageB.float() / 255.0
    # 差分を計算
    C_tensor = B_tensor - A_tensor
    # 結果は0-1範囲のテンソル
    return C_tensor
    
def make_black_pixels_transparent(C_tensor):
    # RGBAのA値（アルファ）を追加して4チャンネルに拡張
    alpha_channel = torch.ones(C_tensor.shape[0], C_tensor.shape[1], 1)  # アルファ値1（不透明）を追加
    
    # RGB (H, W, 3) + Alpha (H, W, 1) -> RGBA (H, W, 4)
    C_tensor_with_alpha = torch.cat([C_tensor, alpha_channel], dim=-1)

    # 黒いピクセル (RGBがすべて0) を探して透明に設定
    black_pixels = torch.all(C_tensor[:, :, :3] == 0, dim=-1)

    # 黒いピクセルのアルファ値を0（透明）に設定
    C_tensor_with_alpha[black_pixels, 3] = 0

    return C_tensor_with_alpha


class SeparateHighlightNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"base image": ("IMAGE",),"lighting image": ("IMAGE",)}
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "separate_highlight"
    CATEGORY = "image"
    OUTPUT_NODE = True
    
    def separate_highlight(self, base_image, lighting_image):
        # 画像AとBの差分画像Cを作成
        C_image = create_difference_image(base_image, lighting_image)
        # 差分画像Cの黒い部分を透明にする
        
        C_image_with_transparency = make_black_pixels_transparent(C_image)
        return C_image_with_transparency

