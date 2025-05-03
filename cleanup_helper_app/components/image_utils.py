# components/image_utils.py
import cv2
import numpy as np
from typing import List, Dict, Optional

def draw_bboxes(
    image: np.ndarray,
    objects: List[Dict],
    current_index: Optional[int] = None
) -> np.ndarray:
    for idx, obj in enumerate(objects):
        x1, y1, x2, y2 = obj["bbox"]
        label = obj["label"]

        if idx == current_index:
            color = (0, 0, 255)  # 赤でハイライト
            thickness = 3
        else:
            color = (0, 255, 0)  # 通常は緑
            thickness = 1

        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return image
