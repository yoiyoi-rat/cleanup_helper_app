# pages/2_Object_Detection.py
import streamlit as st
import numpy as np
from PIL import Image
import cv2
from cleanup_helper_app.models.detector import detect_objects
from cleanup_helper_app.components.image_utils import draw_bboxes

# st.set_page_config(page_title="物体検出", layout="centered")
# st.title("🔍 物体検出")

# # セッション状態の初期化（念のため）
# if "uploaded_image" not in st.session_state or st.session_state["uploaded_image"] is None:
    # st.warning("まず画像をアップロードしてください（1ページ目）")
    # st.stop()

# # OpenCV形式に変換
# file_bytes = st.session_state["uploaded_image"].getvalue()
# np_image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

# # 検出ボタン
# if st.button("物体検出を実行"):
    # with st.spinner("YOLOで検出中..."):
        # detected = detect_objects(np_image)
        # st.session_state["detected_objects"] = detected

    # st.success(f"{len(detected)}個の物体を検出しました！")

    # # バウンディングボックス付きで画像を表示
    # annotated = draw_bboxes(np_image.copy(), detected)
    # st.image(annotated, channels="BGR", caption="検出結果")

# elif st.session_state.get("detected_objects"):
    # # 検出済みの結果を再表示（戻ってきたときの再描画）
    # annotated = draw_bboxes(np_image.copy(), st.session_state["detected_objects"])
    # st.image(annotated, channels="BGR", caption="検出済みの画像")

st.title("🔍 物体検出")

# セッションステートの画像があるか確認
if st.session_state.get("uploaded_image") is None:
    st.warning("先に画像をアップロードしてください。")
    st.stop()

# PIL.Image.Image を取得して numpy 配列に変換
pil_image = st.session_state["uploaded_image"]
image_np = np.array(pil_image.convert("RGB"))

# 物体検出の実行（YOLO）
detected_objects = detect_objects(image_np)
st.session_state["detected_objects"] = detected_objects

# バウンディングボックス付きの画像を表示
image_with_boxes = draw_bboxes(image_np.copy(), detected_objects)
st.image(image_with_boxes, caption="検出結果", use_container_width=True)


# 検出結果をテキストで表示（任意）
st.subheader("検出された物体")
for obj in detected_objects:
    st.write(f"- {obj['label']} at {obj['bbox']}")

# 次に進むボタン
if st.session_state.uploaded_image and st.session_state.mode:
    st.success("物体が検出されました！")
    st.page_link("pages/3_Optimization.py", label="次へ ➡️", icon="➡️")
else:
    st.info("うまく検出が行えませんでした。")
