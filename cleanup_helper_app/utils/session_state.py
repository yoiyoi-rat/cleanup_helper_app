def initialize_session_state(session_state):
    defaults = {
        "mode": None,
        "uploaded_image": None,
        "detected_objects": [],
        "cleanup_plan": [],
        "current_step": 0,
    }
    for key, val in defaults.items():
        if key not in session_state:
            session_state[key] = val
