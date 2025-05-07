import numpy as np
from typing import List, Dict
from scipy.spatial.distance import euclidean
import math
import dimod
from dimod import SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite
from config import DWAVE_API_TOKEN


def solve_cleanup_plan(
    detected_objects: List[Dict],
    mode: str
) -> List[Dict]:
    """
    QUBOを構築して量子アニーリングで最適な片付け順を取得。
    - 入力:
        objects: 検出した物体のリスト [{"label": str, "weight": int, "bbox": [...], "center": (...)}]
        mode: "light" or "heavy"
    - 出力:
        [{"label": str, "weight": int, "order": int, "bbox": [...], "center": (...)}]
    """
    
    N = len(detected_objects)
    Q = {}

    def idx(i, t):
        return (i, t)

    # 制約1：1オブジェクト1回割当て（∑t x_{i,t} = 1）
    PEN_1 = 100
    for i in range(N):
        for t1 in range(N):
            Q[idx(i, t1), idx(i, t1)] = Q.get((idx(i, t1), idx(i, t1)), 0) - PEN_1
            for t2 in range(t1 + 1, N):
                Q[idx(i, t1), idx(i, t2)] = Q.get((idx(i, t1), idx(i, t2)), 0) + 2 * PEN_1
    print("cons 1", 2 * PEN_1)


    # 制約2：各順番に1オブジェクト（∑i x_{i,t} = 1）
    PEN_2 = 100
    for t in range(N):
        for i in range(N):
            Q[idx(i, t), idx(i, t)] = Q.get((idx(i, t), idx(i, t)), 0) - PEN_2
            for j in range(i + 1, N):
                Q[idx(i, t), idx(j, t)] = Q.get((idx(i, t), idx(j, t)), 0) + 2 * PEN_2
    print("cons 2", 2 * PEN_2)


    # 制約3：軽い物を先に片付けたい（重みの逆数）  
    max_w = max(int(obj["weight"]) for obj in detected_objects)
    for i, obj in enumerate(detected_objects):
        inv_w = max_w - int(obj["weight"])
        for t in range(N):
            Q[idx(i, t), idx(i, t)] = Q.get((idx(i, t), idx(i, t)), 0) - inv_w * (N - t) / 3
    print("cons 3", inv_w * (N - t) / 3)


    # 制約4：空間的に近い物体を連続配置（報酬）
    SPATIAL_INC = 3
    centers = [obj["center"] for obj in detected_objects]
    spatial_max = math.hypot(
        max(c[0] for c in centers) - min(c[0] for c in centers),
        max(c[1] for c in centers) - min(c[1] for c in centers)
    ) or 1.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            euclidean_distance = math.hypot(*(np.subtract(centers[i], centers[j])))
            bonus = max(0, SPATIAL_INC * (1 - euclidean_distance / spatial_max))
            for t in range(N - 1):
                Q[idx(i, t), idx(j, t + 1)] = Q.get((idx(i, t), idx(j, t + 1)), 0) - bonus
    print("cons 4", bonus)


    # 制約5：同一ラベルを連続配置（順序的報酬）
    LABEL_INC = 5
    for i in range(N):
        for j in range(N):
            if i != j and detected_objects[i]["label"] == detected_objects[j]["label"]:
                for t in range(N - 1):
                    Q[idx(i, t), idx(j, t + 1)] = Q.get((idx(i, t), idx(j, t + 1)), 0) - LABEL_INC


    # 制約6：重なり・面積に基づく依存制約
    OVLP_PEN = 10
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            x1a, y1a, x2a, y2a = detected_objects[i]["bbox"]
            x1b, y1b, x2b, y2b = detected_objects[j]["bbox"]
            if x1a >= x1b and y1a >= y1b and x2a <= x2b and y2a <= y2b and detected_objects[i]["area"] < detected_objects[j]["area"]:
                for t1 in range(N):
                    for t2 in range(t1 + 1, N):
                        Q[idx(i, t1), idx(j, t2)] = Q.get((idx(i, t1), idx(j, t2)), 0) - OVLP_PEN


    # BinaryQuadraticModel に変換
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)


    #SimulatedAnnealingSampler（実装で削除？）
    # sampler = SimulatedAnnealingSampler()
    # sampleset = sampler.sample(bqm, num_reads=100)

    # DWaveSampler（実装で復活）  # 
    sampler = EmbeddingComposite(DWaveSampler(token=DWAVE_API_TOKEN, solver='Advantage_system4.1'))
    sampleset = sampler.sample(bqm, num_reads=100)


    def optimizer(detected):
        # 最良解の抽出
        best_sample = sampleset.first.sample
        seq = [-1] * N
        for (i, t), val in best_sample.items():
            if val == 1:
                seq[t] = i

        # 結果出力
        result = []
        for rank, i in enumerate(seq, start=1):
            obj = {
                "label": detected[i]["label"],
                "center": detected[i]["center"],
                "bbox": detected[i]["bbox"],
                "order": rank
            }
            result.append(obj)

        return result

    result = optimizer(detected_objects)
    return result