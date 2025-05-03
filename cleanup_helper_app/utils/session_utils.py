# app/utils/session_utils.py
def save_mode_to_session(session_state, mode):
    session_state["mode"] = mode

def save_image_to_session(session_state, image):
    session_state["uploaded_image"] = image
