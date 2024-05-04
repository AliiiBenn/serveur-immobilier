import typing
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/website", StaticFiles(directory="website"), name="website") 

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    """La page d'accueil est la page où se trouvent la liste d'immeubles et appartements"""
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

