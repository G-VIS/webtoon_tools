import torch

def screen_blend(A, C):
    return 1 - (1 - A) * (1 - C)

def create_difference_image(imageA, imageB):
    # 画像が (b, h, w, c) であることを想定し、バッチ次元を含めて差分を計算
    C_tensor = imageB - imageA
    # 結果はそのままバッチ次元を持つテンソル
    return C_tensor


import torch

def make_black_pixels_transparent(C_tensor):
    # C_tensorの形状は (b, h, w, 3) であると想定
    b, h, w, c = C_tensor.shape
    assert c == 3, "入力テンソルのチャンネル数は3 (RGB) である必要があります。"

    # RGBAのA値（アルファ）を追加して4チャンネルに拡張
    alpha_channel = torch.ones(b, h, w, 1, device=C_tensor.device)  # 初期値1（不透明）
    
    # RGB (b, h, w, 3) + Alpha (b, h, w, 1) -> RGBA (b, h, w, 4)
    C_tensor_with_alpha = torch.cat([C_tensor, alpha_channel], dim=-1)  # (b, h, w, 4)

    # 黒いピクセル (RGBがすべて0) を探す
    black_pixels = torch.all(C_tensor >= 0.01, dim=-1, keepdim=True)  # (b, h, w, 1)

    # 黒いピクセルのアルファ値を0（透明）に設定
    C_tensor_with_alpha[black_pixels.expand_as(C_tensor_with_alpha)] = 0

    return C_tensor_with_alpha

    
    
class SeparateHighlightNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "lighting_image": ("IMAGE",)
                }
            }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "separate_highlight"
    CATEGORY = "image"
    OUTPUT_NODE = True
    
    def separate_highlight(self, base_image, lighting_image):
        # バッチ次元を含んだ画像AとBの差分画像Cを作成
        C_image = create_difference_image(base_image, lighting_image)
        # C_imageはバッチ次元を含んだままのテンソル (b, h, w, c)
        return (C_image,)

class SeparateHighlight_BlackTransparencyNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "lighting_image": ("IMAGE",)
                }
            }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "separate_highlight_black_transparency"
    CATEGORY = "image"
    OUTPUT_NODE = True
    def separate_highlight_black_transparency(self, base_image, lighting_image):
        # バッチ次元を含んだ画像AとBの差分画像Cを作成
        C_image = create_difference_image(base_image, lighting_image)
        C_image = make_black_pixels_transparent(C_image)
        return (C_image,)
    