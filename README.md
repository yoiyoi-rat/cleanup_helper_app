# LLM用プロンプト
以下のようなお片付けアプリを作成しています。
アプリの作成では、適切にtestやモックの使用をしながら一つずつ進めていきたいです。
TODOの11以降の部分を実装してください。

# お片付けアプリ
作成したいもの：お片付け補助アプリ（基本的にはスマホからのアクセスを想定している）
概要：ユーザーから部屋の画像を受け取り、その時の体力に応じて、片付けるものとその順番を出力するアプリ

1. ユーザーに軽くorがっつりの2つのオプションを選択してもらう
2. ユーザーに画像を入力or写真を撮影してもらう
3. Yoloを用いて物体検出を行う
4. 物体のリストとそれぞれの片付けコストが記載されたcsvファイルを読み込む
5. 量子アニーリングを用いて、指定コスト内の片付け得点を最大化するように、ある時間（順番）に何を片付けるかを決める。この時、QUBOは以下のように設定する。
- 同じカテゴリのものを片付けるほど高得点
- 近くにあるもの（バウンディングボックスの中心どうしの距離を用いる）を片付けるほど高得点
- 軽くor がっつりに応じて片付けのコストを設定し、各項目ごとに設定されたコストの総和がそのコスト以下になるようにする
- 依存関係の制約を設ける。この時、タスクjを実行する前に依存タスクiが完了しているかの制約は、H = sigma(i, j) sigma t (x_j, t * (1 - sigma (tau < t) x_i, tau))で表せる。この制約は、以下のような制約とする。
ものがほぼほぼ完全に重なっていたら、小さい方の物が大きいもののに乗っていると仮定→小さいものを先に片付けなければならない
そこまで重なっていないようであれば、バウンディングボックスの下の線がより下のものが手前→手前のものを先に片付けなければならない
6. 上記のQUBOからAPIを通して量子アニーリングの機械を使い、片付けるもののリスト（同名のものが複数個あることに注意）とその順番を計算する
7. 「片付けリストが決定しました」という文言と共に、ユーザーがアップした画像と、片付けるものをまず一覧で表示（一枚の画像に、複数のバウンディングボックスがある感じ）
8. 「1. “1番目に片付ける物体の名前”を片付けてください」という文言と同時に、1つ目の物体のバウンディングボックスが表示された写真を表示。ユーザーは終わったら完了ボタンを押す。
9. 「2. “2番目に片付ける物体の名前”を片付けてください」という文言と同時に、1つ目の物体のバウンディングボックスが表示された写真を表示。ユーザーは終わったら完了ボタンを押す。戻るボタンも用意し、前の手順に戻れるようにする。
10. これを片付けるもののリスト分繰り返す（プログレスバーを設置し、ユーザーに進捗を表示する）
11. 「お疲れ様でした！お片付け完了です！」という表示と共に良さそうなアニメーションなどあれば出す。（複雑になるようであれば文字だけで構いません。）

## ディレクトリ構成
```
cleanup_helper_app
├── cleanup_helper_app
│   ├── app.py                         # Streamlit のメインアプリ
│   ├── pages/                          # Streamlit のページ管理用
│   │   ├── 1_Upload_Image.py          # 画像アップロードと設定
│   │   ├── 2_Object_Detection.py      # YOLOによる物体検出
│   │   ├── 3_Optimization.py          # QUBO最適化（量子アニーリング）
│   │   └── 4_Guided_Cleanup.py        # ステップバイステップの片付け誘導
│   ├── components/                    # 再利用可能な部品（画像表示など）
│   │   └── image_utils.py             # 画像描画系（BBの描画など）
│   ├── models/                        # モデルやQUBO設計
│   │   ├── cost_loader.py             # CSV読み込みとマッチング
│   │   ├── detector.py                # YOLOの推論処理
│   │   └── optimizer.py               # QUBO生成＆API送信
│   ├── assets/                        # サンプル画像、CSVなど
│   │   ├── objects.csv
│   │   ├── scatter_girl_room1.jpg
│   │   ├── scatter_girl_room2.jpg
│   │   ├── scatter_oneroom.jpg
│   │   ├── toy_flat.jpg
│   │   ├── toy_heavy.jpeg
│   │   └── toys.jpg
│   └── utils/
│       └── session_state.py        # session_stateのヘルパーなど
├── poetry.lock
├── pyproject.toml
├── pyproject.toml.back
├── README.md
└── tests
    ├── test_cost_loader.py
    ├── test_detector.py
    ├── test_image_utils.py
    ├── test_optimizer.py
    └── test_upload_image.py

```

## TODO
📦 フェーズ1：基本UIと状態構築
ステップ	内容
- ✅ 1	assets/ に画像・CSVを配置 ← 完了
- ✅ 2	tests/ の雛形と最初のテストを書く ← 完了
- ✅ 3	st.session_state の初期化コードを全ページに共通化 ← 完了
- ✅ 4	1_Upload_Image.py：画像アップロード＆モード選択UIを完成 ← 完了
- ✅ 5	テスト：アップロードとモードが正しく session_state に保存されるか確認 ← 完了

🔍 フェーズ2：物体検出（YOLO）関連
ステップ	内容
- ✅6	detector.py：YOLO推論関数 detect_objects(image) を実装 ← 完了
- ✅7	test_detector.py：出力形式の検証テスト ← 完了
- ✅8	2_Object_Detection.py：アップロード画像に対して検出し、結果を session_state に保存 ← 完了

📊 フェーズ3：コストデータと最適化（量子 or 疑似）
ステップ	内容
- ✅9	cost_loader.py：load_cost_table(csv_path) 実装（今ある objects.csv を使う）
- ✅10	test_cost_loader.py：名前とコストの対応テスト
- ✅🔜11	optimizer.py：solve_cleanup_plan(...) の構造を決めてモックで返す
- ✅12	test_optimizer.py：ダミーオブジェクトで最適化ロジックの構造チェック

🧼 フェーズ4：Streamlitによる実行とナビゲーションUI
ステップ	内容
- ✅13	3_Optimization.py：最適化を呼び出し、結果を session_state に保存
- ✅14	4_Guided_Cleanup.py：順番に1つずつ片付けをガイド（BB表示つき）
- ✅15	image_utils.py：draw_bboxes() 実装し、現在の物体を強調表示
- ✅16	プログレスバー、完了ボタン、戻るボタンの導入

🚀 フェーズ5：デプロイと仕上げ
ステップ	内容
- 17	UIのモバイル対応調整（layout="centered" やボタン配置など）
- 18	requirements.txt、.streamlit/config.toml の整備
- 19	VercelでStreamlitをデプロイ（streamlit-component-templateを使う）
- 20	READMEの整備とバグ取り・改善ループ

## object.csvの形式
```
id,label,is_in_home,is_furniture,weight,label_jp
0,Accordion,1,0,3,アコーディオン
1,Adhesive tape,1,0,1,粘着テープ
2,Aircraft,0,0,,航空機
3,Airplane,0,0,,飛行機
```

## アプリの立ち上げ方
```
poetry run streamlit run cleanup_helper_app/app.py --server.enableCORS false --server.enableXsrfProtection false --server.address 0.0.0.0
```

## 設計されている関数
**models/detector.py**

def _load_model():
def detect_objects(image: np.ndarray) -> List[Dict]:
    """
    YOLOを使って物体検出を行う。
    - 入力: OpenCV画像（np.ndarray）
    - 出力: [{"label": str, "bbox": [x1, y1, x2, y2], "center": (x, y)}]
    """

**components/image_utils.py**
def draw_bboxes(
    image: np.ndarray,
    objects: List[Dict],
    current_index: Optional[int] = None
) -> np.ndarray:

**utils/session_state.py**
def initialize_session_state(session_state):
    session_stateが{
        "mode": None,
        "uploaded_image": None,
        "detected_objects": [],
        "cleanup_plan": [],
        "current_step": 0,
    }になる

**models/cost_loader.py**
def load_cost_table(csv_path: str) -> pd.DataFrame:
    """
    物体の情報が記載されたCSVを読み込み、必要な整形をしてDataFrameで返す。
    Args:
        csv_path (str): CSVファイルのパス
    Returns:
        pd.DataFrame: 整形済みデータフレーム
    """