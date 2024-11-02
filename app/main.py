import pathlib
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))

now = datetime.datetime.now()
@app.get("/", response_class=HTMLResponse) # GET
def home_view(request: Request):
        return templates.TemplateResponse("home.html", {"request": request, "abc": now.strftime("%H:%M")}) #path is relative to template dir

@app.post("/") #POST
def home_detail_view():
        return {"hello":"world"}