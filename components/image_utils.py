def draw_bboxes(
    image: np.ndarray,
    objects: List[Dict],
    current_index: Optional[int] = None
) -> np.ndarray:
    """
    バウンディングボックスを画像上に描画（現在の注目物体をハイライト）
    - 入力: 元画像、検出物体、現在のステップインデックス
    - 出力: 描画済画像
    """
