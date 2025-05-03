import streamlit as st
from utils.session_state import initialize_session_state

initialize_session_state(st.session_state)

st.set_page_config(page_title="お片付け補助アプリ", layout="centered")

st.title("お片付け補助アプリ 🧹")
st.write("スマホから写真をアップロードして、片付ける順番をガイドします！")

st.page_link("pages/1_Upload_Image.py", label="▶️ 画像をアップロード", icon="📷")
st.page_link("pages/2_Object_Detection.py", label="▶️ 物体検出を実行", icon="🔍")
st.page_link("pages/3_Optimization.py", label="▶️ 最適な片付け順を計算", icon="🧠")
st.page_link("pages/4_Guided_Cleanup.py", label="▶️ 片付けステップへ", icon="✅")

