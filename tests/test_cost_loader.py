# def test_load_cost_table_valid():
    # from cleanup_helper_app.models.cost_loader import load_cost_table
    # result = load_cost_table("cleanup_helper_app/assets/objects.csv")
    # assert isinstance(result, dict)
    # assert "bottle" in result
import pandas as pd
import pytest
from cleanup_helper_app.models.cost_loader import load_cost_table
import tempfile
import os

# モックCSVデータ（テスト用）
MOCK_CSV = """id,name,jp_name,likely_in_room_flag,furniture_flag,weight_cost
0,Accordion,アコーディオン,1,0,3
1,Adhesive tape,粘着テープ,1,0,1
2,Aircraft,航空機,0,0,
3,Table,テーブル,1,1,5
4,Unknown Item,不明,,
"""

def create_temp_csv(content: str):
    """一時ファイルとしてCSVを作成してパスを返す"""
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv')
    tmp.write(content)
    tmp.close()
    return tmp.name

def test_load_cost_table_success():
    csv_path = create_temp_csv(MOCK_CSV)
    df = load_cost_table(csv_path)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 5
    assert all(col in df.columns for col in ["id", "name", "jp_name", "likely_in_room_flag", "furniture_flag", "weight_cost"])
    assert df.loc[2, "weight_cost"] == 0  # 欠損が0で埋められている
    assert df.loc[4, "likely_in_room_flag"] == 0  # 欠損が0で埋められている
    assert df.loc[3, "furniture_flag"] == 1
    os.remove(csv_path)

def test_load_cost_table_missing_columns():
    bad_csv = """id,name,jp_name
0,Accordion,アコーディオン
"""
    csv_path = create_temp_csv(bad_csv)
    with pytest.raises(ValueError) as excinfo:
        load_cost_table(csv_path)
    assert "CSVに必要なカラムが存在しません" in str(excinfo.value)
    os.remove(csv_path)
