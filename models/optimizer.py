def solve_cleanup_plan(
    objects: List[Dict],
    cost_table: Dict[str, Dict],
    mode: str  # "light" or "intense"
) -> List[Dict]:
    """
    QUBOを構築して量子アニーリングで最適な片付け順を取得。
    - 入力:
        objects: 物体検出されたラベル・位置情報リスト
        cost_table: コスト/カテゴリ辞書
        mode: 軽く or がっつり
    - 出力:
        [{"label": str, "order": int, "bbox": [...], "center": (...)}]
    """
