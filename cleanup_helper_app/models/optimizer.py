import numpy as np
from typing import List, Dict
from scipy.spatial.distance import euclidean

def solve_cleanup_plan(
    detected_objects: List[Dict],
    cost_table: Dict[str, int],
    mode: str = "light"
) -> List[Dict]:
    mode_cost_limit = {"light": 10, "full": 40}
    max_cost = mode_cost_limit.get(mode, 5)

    # コスト付与（なければデフォルト2）
    for obj in detected_objects:
        obj["cost"] = cost_table.get(obj["label"], 2)

    # 類似性スコア（ラベルが同じなら +3）
    def similarity_score(obj1, obj2):
        return 3 if obj1["label"] == obj2["label"] else 0

    # 距離スコア（中心座標が近いほどスコア高）
    def distance_score(obj1, obj2):
        d = euclidean(obj1["center"], obj2["center"])
        return 5 / (d + 1e-3)  # 小さい距離ほど高スコア

    # 総合スコア = similarity + distance
    n = len(detected_objects)
    scores = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_score(detected_objects[i], detected_objects[j])
            dist = distance_score(detected_objects[i], detected_objects[j])
            scores[i, j] = scores[j, i] = sim + dist

    # 貪欲法で高スコア順に物体を選択（制限内まで）
    selected = []
    total_cost = 0
    remaining = list(range(n))

    while remaining:
        best_idx = max(remaining, key=lambda i: sum(scores[i][j] for j in selected) if selected else 0)
        obj = detected_objects[best_idx]
        if total_cost + obj["cost"] <= max_cost:
            selected.append(best_idx)
            total_cost += obj["cost"]
        remaining.remove(best_idx)

    # 順番を決定（簡易：距離が手前の順）
    ordered = sorted(selected, key=lambda i: detected_objects[i]["center"][1])
    result = []
    for order, idx in enumerate(ordered, 1):
        obj = detected_objects[idx]
        obj["order"] = order
        result.append(obj)

    return result


# def solve_cleanup_plan(
    # detected_objects: List[Dict],
    # cost_table: Dict[str, int],
    # mode: str = "light"
# ) -> List[Dict]:
    # """
    # 与えられた物体リストとコスト情報、片付けモードに基づき、
    # 片付けの順番を含む最適な片付け計画を返す（モック）

    # Args:
        # detected_objects (List[Dict]): YOLOで検出された物体 [{"label": str, "bbox": [...], "center": (...)}, ...]
        # cost_table (Dict[str, int]): ラベル名 -> コスト
        # mode (str): "light" or "full"

    # Returns:
        # List[Dict]: [{"label": str, "bbox": [...], "order": int}, ...]
    # """
    # # モック実装：単純にコスト順にソートして順番をつける
    # mode_cost_limit = {"light": 5, "full": 15}
    # max_cost = mode_cost_limit.get(mode, 5)

    # # 各物体にコストを付与（なければデフォルト2）
    # for obj in detected_objects:
        # obj["cost"] = cost_table.get(obj["label"], 2)

    # # コスト制限内でできるだけ多く片付けるように
    # total_cost = 0
    # selected = []
    # for obj in sorted(detected_objects, key=lambda x: x["cost"]):
        # if total_cost + obj["cost"] <= max_cost:
            # selected.append(obj)
            # total_cost += obj["cost"]

    # # 順番を振って返す
    # for i, obj in enumerate(selected):
        # obj["order"] = i + 1

    # return selected


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