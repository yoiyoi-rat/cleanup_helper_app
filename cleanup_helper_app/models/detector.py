# models/detector.py
from typing import List, Dict
import numpy as np
import pandas as pd
from ultralytics import YOLO
import os
import torch
from .cost_loader import load_cost_table
from ..config import OBJECTS_CSV_PATH

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

# グローバル変数でモデルを1回だけ読み込む
_model = None


def _load_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "weights", "yolov8x-oiv7.pt")
        _model = YOLO(model_path)
    return _model


def _load_cost_table_filtered() -> pd.DataFrame:
    """
    is_in_home == 1 かつ is_furniture == 0 の行だけを返す。
    """
    df = load_cost_table(OBJECTS_CSV_PATH)
    df = df[(df["is_in_home"] == 1) & (df["is_furniture"] == 0)]
    return df


def compute_iou(box1, box2):
    """
    重なっている部分を計算
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # 計算交差領域
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    if inter_area == 0:
        return 0.0

    # 計算各ボックスの面積
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # IoU 計算
    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou


def remove_overlapping_detections(detections, iou_threshold=0.8):
    """
    重なっているobjectを排除
    """
    filtered = []
    used = [False] * len(detections)

    for i, det_i in enumerate(detections):
        if used[i]:
            continue
        keep = True
        for j, det_j in enumerate(detections):
            if i == j or used[j]:
                continue
            if compute_iou(det_i["bbox"], det_j["bbox"]) > iou_threshold:
                # 重複と見なす。ここでは大きい面積の方を優先。
                if det_i["area"] < det_j["area"]:
                    keep = False
                    break
                else:
                    used[j] = True
        if keep:
            filtered.append(det_i)
            used[i] = True
    return filtered



def detect_objects(image: np.ndarray) -> List[Dict]:
    """
    YOLOで物体検出し、フィルタ条件に合致したもののみ返す。
    """
    model = _load_model()
    results = model.predict(image, imgsz=1280, conf=0.05, verbose=False)[0]

    filtered_df = _load_cost_table_filtered()
    filtered_labels = set(filtered_df["label"])

    # filtered_df全体をlabelとweightのマッピング辞書に変換
    label_to_weight = dict(zip(filtered_df["label"], filtered_df["weight"]))

    detected = []
    for box in results.boxes:
        cls_id = int(box.cls.item())
        label = model.names[cls_id]

        if label not in filtered_labels:
            continue  # フィルタ条件に合わないので除外

        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        detected.append({
            "label": label,
            "weight": label_to_weight.get(label),
            "bbox": [x1, y1, x2, y2],
            "center": center,
            "area": (int(x2) - int(x1)) * (int(y2) - int(y1))
        })
    
    not_overlap_detected = remove_overlapping_detections(detected, iou_threshold=0.8)
    sorted_detected = sorted(not_overlap_detected, key=lambda x: x["weight"])
    cut_detected = sorted_detected[:10]



    return cut_detected

