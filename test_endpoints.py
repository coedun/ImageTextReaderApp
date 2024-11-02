from fastapi.testclient import TestClient
from app.main import app, BASE_DIR, UPLOAD_DIR
import shutil
import time
import io
from PIL import Image, ImageChops

client = TestClient(app)

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']

def test_invalid_file_error():
    response = client.post("/")
    assert response.status_code == 422
    assert 'application/json' in response.headers['content-type']


def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/img-echo/", files={"file": open(path, 'rb')})
        fext = str(path.suffix).replace('.', '')
        if img is None:
            assert response.status_code == 400
        else:
            # returning a valid image
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()

            assert difference is None

def test_prediction_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/", files={"file": open(path, 'rb')})
        fext = str(path.suffix).replace('.', '')
        if img is None:
            assert response.status_code == 400
        else:
            # returning a valid image
            assert response.status_code == 200
            data = response.json()
            print(data)
            assert len(data.keys()) ==2

    #time.sleep(3)
    shutil.rmtree(UPLOAD_DIR)