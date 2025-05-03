# components/image_utils.py
import cv2
import numpy as np
from typing import List, Dict, Optional

import cv2
import numpy as np
from typing import List, Dict, Optional


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


# def draw_bboxes(
    # image: np.ndarray,
    # objects: List[Dict],
    # current_index: Optional[int] = None
# ) -> np.ndarray:
    # for idx, obj in enumerate(objects):
        # x1, y1, x2, y2 = obj["bbox"]
        # label = obj["label"]

        # if idx == current_index:
            # color = (0, 0, 255)  # 赤でハイライト
            # thickness = 3
        # else:
            # color = (0, 255, 0)  # 通常は緑
            # thickness = 1

        # cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        # cv2.putText(image, label, (x1, y1 - 10),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    # return image
