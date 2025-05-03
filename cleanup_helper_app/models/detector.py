# models/detector.py
from typing import List, Dict
import numpy as np
from ultralytics import YOLO
import os
import torch

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

# グローバル変数でモデルを1回だけ読み込む
_model = None

def _load_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "weights", "yolov8n-oiv7.pt")
        _model = YOLO(model_path)
    return _model

def detect_objects(image: np.ndarray) -> List[Dict]:
    """
    YOLOを使って物体検出を行う。
    - 入力: OpenCV画像（np.ndarray）
    - 出力: [{"label": str, "bbox": [x1, y1, x2, y2], "center": (x, y)}]
    """
    model = _load_model()
    results = model.predict(image, imgsz=640, verbose=False)[0]

    detected = []
    for box in results.boxes:
        cls_id = int(box.cls.item())
        label = model.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        detected.append({
            "label": label,
            "bbox": [x1, y1, x2, y2],
            "center": center
        })

    return detected

# mock
# def detect_objects(image: np.ndarray) -> List[Dict]:
    # """
    # YOLOを使って物体検出を行う。
    # - 入力: OpenCV画像（np.ndarray）
    # - 出力: [{"label": str, "bbox": [x1, y1, x2, y2], "center": (x, y)}]
    # """
    # h, w, _ = image.shape
    # return [
        # {
            # "label": "ぬいぐるみ",
            # "bbox": [int(w*0.1), int(h*0.1), int(w*0.3), int(h*0.4)],
            # "center": (int((w*0.1 + w*0.3)/2), int((h*0.1 + h*0.4)/2)),
        # },
        # {
            # "label": "クッション",
            # "bbox": [int(w*0.5), int(h*0.5), int(w*0.7), int(h*0.7)],
            # "center": (int((w*0.5 + w*0.7)/2), int((h*0.5 + h*0.7)/2)),
        # }
    # ]

