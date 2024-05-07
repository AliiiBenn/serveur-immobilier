from fastapi.responses import HTMLResponse
from core.api.auth import get_current_user_from_cookie

from fastapi import Depends, Request, APIRouter
from fastapi.templating import Jinja2Templates


from core.api.models import Compte


router = APIRouter()
templates = Jinja2Templates(directory="../templates")




@router.get("/immeubles", response_class=HTMLResponse)
async def get_immeubles(request: Request, user: Compte = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("immeubles.html", {"user": user, "request": request})