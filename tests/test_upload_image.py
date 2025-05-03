# tests/test_upload_image.py
import pytest
from PIL import Image
from io import BytesIO
from cleanup_helper_app.utils.session_utils import save_mode_to_session, save_image_to_session

@pytest.fixture
def dummy_session():
    return {}

def test_save_mode_to_session(dummy_session):
    save_mode_to_session(dummy_session, "がっつり")
    assert dummy_session["mode"] == "がっつり"

def test_save_image_to_session(dummy_session):
    # モック画像作成
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    save_image_to_session(dummy_session, img)
    assert dummy_session["uploaded_image"] == img
