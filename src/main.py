from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from core.api.auth import get_current_user_from_cookie

import routers.login as login
import routers.immeubles as immeubles

from core.api.engine import Engine

Engine().create_all()

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

app.include_router(login.router)
app.include_router(immeubles.router)






@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)




