# pages/1_Upload_Image.py
import streamlit as st
from PIL import Image
from components.image_utils import resize_image_by_short_side
import numpy as np

st.set_page_config(page_title="画像アップロードとモード選択", layout="centered")

st.title("お片付けアシスタント 🧹")
st.subheader("今日のお片付けはどのくらい？")

# 表示用 → 内部用マッピング
mode_map = {"軽く": "light", "がっつり": "hard"}

# 表示と選択
selected = st.radio("片付けモードを選んでください", ["軽く", "がっつり"], horizontal=True)
st.session_state.mode = mode_map[selected]
mode = st.session_state.mode  # "light" または "hard"

# 画像アップロード or 撮影（スマホ対応）
uploaded_file = st.file_uploader("部屋の画像をアップロード", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    resized_image = resize_image_by_short_side(image)
    st.image(resized_image, caption="アップロードされた画像", use_container_width=True)
    st.session_state.uploaded_image = resized_image

# 次に進むボタン
if st.session_state.uploaded_image and st.session_state.mode:
    st.success("モードと画像が設定されました！")
    st.page_link("pages/2_Object_Detection.py", label="次へ ➡️", icon="➡️")
else:
    st.info("モードと画像の両方を設定してください。")
