import streamlit as st
from models.cost_loader import load_cost_table
from models.optimizer import solve_cleanup_plan


st.set_page_config(page_title="最適化", layout="centered")
st.title("🧠 最適な片付け順を計算中...")

# 前ステップで必要な情報があるか確認
if not st.session_state["detected_objects"] or not st.session_state["uploaded_image"]:
    st.warning("画像と物体検出の情報が必要です。先にステップ1と2を完了してください。")
    st.stop()

# 最適化を実行（モック）
st.info("最適化アルゴリズムを実行しています...")
cleanup_plan = solve_cleanup_plan(
    detected_objects=st.session_state["detected_objects"],
    mode=st.session_state["mode"]
)

# 結果を保存
st.session_state["cleanup_plan"] = cleanup_plan

st.success("片付け順が決定しました！次のステップへ進んでください。")
st.write("---")

if st.button("📋 ステップバイステップ片付けへ進む"):
    st.switch_page("pages/4_Guided_Cleanup.py")

