# お片付けアプリ

## ディレクトリ構成
```
cleanup_helper_app/
├── app.py                         # Streamlit のメインアプリ
├── pages/                         # Streamlit のページ管理用
│   ├── 1_Upload_Image.py          # 画像アップロードと設定
│   ├── 2_Object_Detection.py      # YOLOによる物体検出
│   ├── 3_Optimization.py          # QUBO最適化（量子アニーリング）
│   └── 4_Guided_Cleanup.py        # ステップバイステップの片付け誘導
├── components/                    # 再利用可能な部品（画像表示など）
│   └── image_utils.py             # 画像描画系（BBの描画など）
├── models/                        # モデルやQUBO設計
│   ├── detector.py                # YOLOの推論処理
│   ├── cost_loader.py             # CSV読み込みとマッチング
│   └── optimizer.py               # QUBO生成＆API送信
├── assets/                        # サンプル画像、CSVなど
│   ├── object_costs.csv
│   └── sample_room.jpg
├── requirements.txt              # 依存ライブラリ
└── README.md

```