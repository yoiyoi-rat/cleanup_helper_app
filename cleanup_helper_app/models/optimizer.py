from typing import List, Dict


def solve_cleanup_plan(
    detected_objects: List[Dict],
    cost_table: Dict[str, int],
    mode: str = "light"
) -> List[Dict]:
    """
    与えられた物体リストとコスト情報、片付けモードに基づき、
    片付けの順番を含む最適な片付け計画を返す（モック）

    Args:
        detected_objects (List[Dict]): YOLOで検出された物体 [{"label": str, "bbox": [...], "center": (...)}, ...]
        cost_table (Dict[str, int]): ラベル名 -> コスト
        mode (str): "light" or "full"

    Returns:
        List[Dict]: [{"label": str, "bbox": [...], "order": int}, ...]
    """
    # モック実装：単純にコスト順にソートして順番をつける
    mode_cost_limit = {"light": 5, "full": 15}
    max_cost = mode_cost_limit.get(mode, 5)

    # 各物体にコストを付与（なければデフォルト2）
    for obj in detected_objects:
        obj["cost"] = cost_table.get(obj["label"], 2)

    # コスト制限内でできるだけ多く片付けるように
    total_cost = 0
    selected = []
    for obj in sorted(detected_objects, key=lambda x: x["cost"]):
        if total_cost + obj["cost"] <= max_cost:
            selected.append(obj)
            total_cost += obj["cost"]

    # 順番を振って返す
    for i, obj in enumerate(selected):
        obj["order"] = i + 1

    return selected


# def solve_cleanup_plan(
    # objects: List[Dict],
    # cost_table: Dict[str, Dict],
    # mode: str  # "light" or "intense"
# ) -> List[Dict]:
    # """
    # QUBOを構築して量子アニーリングで最適な片付け順を取得。
    # - 入力:
        # objects: 物体検出されたラベル・位置情報リスト
        # cost_table: コスト/カテゴリ辞書
        # mode: 軽く or がっつり
    # - 出力:
        # [{"label": str, "order": int, "bbox": [...], "center": (...)}]
    # """