# pages/1_Upload_Image.py
import streamlit as st
from PIL import Image
from utils.session_state import initialize_session_state

initialize_session_state(st.session_state)

st.set_page_config(page_title="画像アップロードとモード選択", layout="centered")

st.title("お片付けアシスタント 🧹")
st.subheader("今日のお片付けはどのくらい？")

# ステート初期化
if "mode" not in st.session_state:
    st.session_state.mode = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# 軽く or がっつりの選択
mode = st.radio("片付けモードを選んでください", ["軽く", "がっつり"], horizontal=True)
st.session_state.mode = mode

# 画像アップロード or 撮影（スマホ対応）
uploaded_file = st.file_uploader("部屋の画像をアップロード", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)
    st.session_state.uploaded_image = image

# 次に進むボタン
if st.session_state.uploaded_image and st.session_state.mode:
    st.success("モードと画像が設定されました！")
    st.page_link("pages/2_Object_Detection.py", label="次へ ➡️", icon="➡️")
else:
    st.info("モードと画像の両方を設定してください。")
