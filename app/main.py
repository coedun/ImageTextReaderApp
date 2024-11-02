import pathlib
import datetime
import uuid
import io
from functools import lru_cache
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request,
    File,
    UploadFile
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
from PIL import Image
import pytesseract
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
            env_file = ".env"

@lru_cache
def get_settings():
    return Settings()


DEBUG=get_settings().debug
BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))

now = datetime.datetime.now()
@app.get("/", response_class=HTMLResponse) # GET
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request, "abc": now.strftime("%H:%M")}) #path is relative to template dir

@app.post("/") #POST
async def prediction_view(file: UploadFile = File(...), settings:Settings = Depends(get_settings)):

    bytes_str = io.BytesIO(await file.read())

    try:
        img = Image.open(bytes_str)
    except:
         raise HTTPException(detail="Invalid image", status_code=400)

    preds = pytesseract.image_to_string(img)
    predictions = [x for x in preds.split("\n")]

    return {"results": predictions, "original": preds}


# image uploading methods
@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file: UploadFile = File(...), settings:Settings = Depends(get_settings)):
    if not settings.echo_active:
         raise HTTPException(detail="Invalid endpoint", status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())

    try:
        img = Image.open(bytes_str)
    except:
         raise HTTPException(detail="Invalid image", status_code=400)

    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"

    img.save(dest)
    return dest