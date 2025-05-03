import numpy as np
from cleanup_helper_app.models.detector import detect_objects

def test_detect_objects_format():
    dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
    results = detect_objects(dummy_image)

    assert isinstance(results, list)
    for obj in results:
        assert "label" in obj and isinstance(obj["label"], str)
        assert "bbox" in obj and isinstance(obj["bbox"], list) and len(obj["bbox"]) == 4
        assert "center" in obj and isinstance(obj["center"], tuple) and len(obj["center"]) == 2
