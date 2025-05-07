import streamlit as st
import cv2
import PIL
import numpy as np
from components.image_utils import draw_bboxes
from typing import List, Dict, Optional
import hashlib


@st.cache_data
def get_drawn_image_bytes(image_array: np.ndarray, cleanup_plan: List[Dict], current_index: int) -> bytes:
    # ハッシュ用に cleanup_plan を文字列に
    plan_hash = hashlib.md5(str(cleanup_plan).encode() + str(current_index).encode()).hexdigest()

    # 画像はリサイズ済み前提
    drawn = draw_bboxes(image_array.copy(), cleanup_plan, current_index)
    _, img_encoded = cv2.imencode(".jpg", drawn)
    return img_encoded.tobytes()


st.set_page_config(page_title="片付けステップ", layout="centered")
st.title("🧹 片付けステップバイステップ")

if not st.session_state["uploaded_image"] or not st.session_state["cleanup_plan"]:
    st.warning("画像と片付け順が必要です。前のステップを完了してください。")
    st.stop()

cleanup_plan = st.session_state["cleanup_plan"]
cleanup_plan = sorted(cleanup_plan, key=lambda x: x["order"])
current_step = st.session_state["current_step"]

# 終了判定
if current_step >= len(cleanup_plan):
    st.success("🎉 お疲れ様でした！お片付け完了です！")
    st.balloons()

    # 🔙 戻るボタン
    if st.button("最後のステップに戻る"):
        st.session_state["current_step"] = len(cleanup_plan) - 1
        st.rerun()
    st.stop()

# 対象物体の取得
current_object = cleanup_plan[current_step]

# 画像の取得と描画
image_data = st.session_state["uploaded_image"]
if isinstance(image_data, PIL.Image.Image):
    image = cv2.cvtColor(np.array(image_data), cv2.COLOR_RGB2BGR)
else:
    st.error("画像の形式が不正です。")
    st.stop()

# drawn_image = draw_bboxes(image.copy(), cleanup_plan, current_index=current_step)
# st.image(drawn_image, caption=f"{current_step+1}. {current_object['label']} を片付けてください", channels="BGR")

# キャッシュ付きで画像描画（バイト列で表示）
image_bytes = get_drawn_image_bytes(image, cleanup_plan, current_index=current_step)
st.image(image_bytes, caption=f"{current_step+1}. {current_object['label']} を片付けてください", channels="BGR")


# プログレスバー
progress = int((current_step + 1) / len(cleanup_plan) * 100)
st.progress(progress, text=f"進捗: {current_step+1} / {len(cleanup_plan)}")

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ 完了！次へ"):
        st.session_state["current_step"] += 1
        st.rerun()
with col2:
    if current_step > 0 and st.button("⬅️ 戻る"):
        st.session_state["current_step"] -= 1
        st.rerun()
