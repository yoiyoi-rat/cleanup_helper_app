# components/image_utils.py
import cv2
import numpy as np
from typing import List, Dict, Optional
from PIL import Image


def draw_bboxes(
    image: np.ndarray,
    objects: List[Dict],
    current_index: Optional[int] = None
) -> np.ndarray:
    """
    バウンディングボックスを画像に描画する。
    current_index が指定されている場合、その物体を強調表示する。
    """
    for idx, obj in enumerate(objects):
        label = obj.get("label", "")
        x1, y1, x2, y2 = obj.get("bbox", [0, 0, 0, 0])

        if idx == current_index:
            color = (0, 0, 255)  # 赤（現在の対象）
            thickness = 4
        else:
            color = (0, 255, 0)  # 緑（その他）
            thickness = 2

        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        cv2.putText(
            image,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            lineType=cv2.LINE_AA
        )

    return image


# def resize_image_by_short_side(image: np.ndarray, short_side=640) -> np.ndarray:
    # height, width = image.shape[:2]
    # if min(height, width) == short_side:
        # return image  # すでに希望のサイズ

    # # 縮小スケールを計算（短辺基準）
    # scale = short_side / min(height, width)
    # new_width = int(width * scale)
    # new_height = int(height * scale)
    # resized = cv2.resize(image, (new_width, new_height))
    # return resized


def resize_image_by_short_side(image: Image.Image, short_side=640) -> Image.Image:
    width, height = image.size  # PILは (幅, 高さ)
    
    if min(height, width) == short_side:
        return image  # すでに希望のサイズ
    
    # スケール計算（短辺基準）
    scale = short_side / min(height, width)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # LANCZOSを使ってリサイズ
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized
