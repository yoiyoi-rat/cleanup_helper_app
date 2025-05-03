# def load_cost_table(path: str) -> dict[str, dict]:
    # """
    # CSVから物体ラベルに対応する片付けコスト等を読み込む。
    # - 入力: CSVパス
    # - 出力: {"bottle": {"cost": 3, "category": "plastic", ...}, ...}
    # """
import pandas as pd

def load_cost_table(csv_path: str) -> pd.DataFrame:
    """
    物体の情報が記載されたCSVを読み込み、必要な整形をしてDataFrameで返す。
    Args:
        csv_path (str): CSVファイルのパス
    Returns:
        pd.DataFrame: 整形済みデータフレーム
    """
    df = pd.read_csv(csv_path)

    # ✅ 必須カラムチェック
    required_columns = ["id", "name", "jp_name", "likely_in_room_flag", "furniture_flag", "weight_cost"]
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"CSVに必要なカラムが存在しません: {missing}")

    # 正常処理
    df["likely_in_room_flag"] = df["likely_in_room_flag"].fillna(0).astype(int)
    df["furniture_flag"] = df["furniture_flag"].fillna(0).astype(int)
    df["weight_cost"] = pd.to_numeric(df["weight_cost"], errors="coerce").fillna(0).astype(int)
    return df
