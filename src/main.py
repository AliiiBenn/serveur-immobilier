from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from core.api.auth import get_current_user_from_cookie

import routers.login.router as router_login
import routers.immeubles.router as router_immeubles
import routers.syndicats.router as router_syndicats
import routers.appartements.router as appartements



app = FastAPI()
templates = Jinja2Templates(directory="../templates")

app.include_router(router_login.router)
app.include_router(router_immeubles.router)
app.include_router(router_syndicats.router)
app.include_router(appartements.router)


    
from core.api.crud import ImmeubleCRUD

crud = ImmeubleCRUD()


    


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



