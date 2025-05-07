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
    required_columns = ["id", "label", "label_jp", "is_in_home", "is_furniture", "weight"]
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"CSVに必要なカラムが存在しません: {missing}")

    # 正常処理
    df["is_in_home"] = df["is_in_home"].fillna(0).astype(bool)
    df["is_furniture"] = df["is_furniture"].fillna(1).astype(bool)
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce").fillna(100).astype(int) # 選ばれないようにでかく
    return df
