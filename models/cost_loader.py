def load_cost_table(path: str) -> Dict[str, Dict]:
    """
    CSVから物体ラベルに対応する片付けコスト等を読み込む。
    - 入力: CSVパス
    - 出力: {"bottle": {"cost": 3, "category": "plastic", ...}, ...}
    """
