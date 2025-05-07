"""
アプリケーション設定を管理するモジュール
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# アプリケーションのベースディレクトリを取得
# __file__はこのファイル（config.py）の場所を指す
BASE_DIR = Path(__file__).parent.parent

APP_DIR = os.path.join(BASE_DIR, "cleanup_helper_app") 

ASSETS_DIR = os.path.join(APP_DIR, "assets")

# オブジェクトリストファイルのパス
OBJECTS_CSV_PATH = os.path.join(ASSETS_DIR, "objects.csv")


# .env ファイルを読み込む
load_dotenv()

# トークンを環境変数から取得
DWAVE_API_TOKEN = os.getenv("DWAVE_API_TOKEN")