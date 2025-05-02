def detect_objects(image: np.ndarray) -> List[Dict]:
    """
    YOLOを使って物体検出を行う。
    - 入力: OpenCV画像（np.ndarray）
    - 出力: [{"label": str, "bbox": [x1, y1, x2, y2], "center": (x, y)}]
    """
