from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from core.api.crud import SyndicatCRUD
from core.api.models import Proprietaire, Syndicat
from core.api.auth import get_current_user_from_cookie
from core.api.engine import Engine

from .forms import SyndicatForm


router = APIRouter()
engine = Engine()
templates = Jinja2Templates(directory="../templates")

crud = SyndicatCRUD()




@router.get(
    path="/syndicats",
    response_class=HTMLResponse,
    description="Affiche tous les syndicats du client actuel (en fonction de son identifiant)"
)
async def get_syndicats(request: Request, user: Proprietaire = Depends(get_current_user_from_cookie)):
    syndicats = crud.get_all_syndicats(user.identifiant)
        
    return templates.TemplateResponse("syndicats.html", {"user": user, "request": request, "syndicats": syndicats})
    
    



@router.get(
    path="/syndicats/nouveau",
    response_class=HTMLResponse,
    description="Affiche la page de création d'un syndicat. Liée à une requête POST"
)
async def syndicats_nouveau_get(request: Request, user: Proprietaire = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("syndicat_nouveau.html", {"request": request, "user": user})


@router.get(
    path="/syndicats/{id}", 
    response_class=HTMLResponse,
    description="Affiche les données d'un syndicat indivuduel"
)
async def syndicats_id_get(request: Request,
                           user: Proprietaire = Depends(get_current_user_from_cookie),
                           syndicat: Syndicat = Depends(crud.get_syndicat_from_id)):
    
    immeubles = crud.get_immeubles_of_syndicat(syndicat)
    return templates.TemplateResponse("syndicat.html", {"user": user, "request": request, "syndicat": syndicat, "immeubles": immeubles})


@router.post(
    path="/syndicats/nouveau", 
    response_class=HTMLResponse,
    description="Ajoute un syndicat à la base de données et redirige vers la page des syndicats"
)
async def syndicats_nouveau_post(request: Request, user: Proprietaire = Depends(get_current_user_from_cookie)):
    form = SyndicatForm(request)
    await form.load_data()
    
    syndicat = Syndicat(
                nom=form.nom,
                adresse=form.adresse,
                telephone=form.telephone,
                email=form.email,
                id_referente=user.identifiant
            )
    exists = SyndicatCRUD().syndicat_exists(syndicat, user.identifiant)
    
    if await form.validate() and not exists:
        crud.add_syndicat(syndicat)
        
    
    return await get_syndicats(request, user)



