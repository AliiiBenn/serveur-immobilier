from __future__ import annotations

from typing import Final, Sequence
from functools import wraps


from fastapi.responses import HTMLResponse
from core.api.auth import get_current_user_from_cookie

from fastapi import Depends, Request, APIRouter
from fastapi.templating import Jinja2Templates


from core.api.models import Locataire, Proprietaire, Immeuble, Appartement
from core.api.auth import get_current_user_from_cookie
from core.api.engine import Engine
from core.api.crud import ImmeubleCRUD, SyndicatCRUD, AppartementCRUD, LocataireCRUD

from .forms import ImmeubleForm, create_immeuble_from_form

from routers.appartements.forms import AppartementForm


router = APIRouter()
templates = Jinja2Templates(directory="../templates")
engine = Engine()

crud_immeubles = ImmeubleCRUD()
crud_syndicats = SyndicatCRUD()
crud_appartements = AppartementCRUD()
crud_locataires = LocataireCRUD()


class AppartementAvecLocataires:
    def __init__(self, appartement : Appartement, locataires : Sequence[Locataire]):
        self.appartement = appartement
        self.locataires = locataires
        self.est_loue = len(locataires) > 0
        
    
    @classmethod
    def from_immeuble(cls, immeuble : Immeuble) -> Sequence[AppartementAvecLocataires]:
        result : list[AppartementAvecLocataires] = []
        
        appartements = crud_appartements.get_appartements_from_immeuble(immeuble.identifiant)
        
        for appartement in appartements:
            locataires = crud_locataires.get_locataires_from_appartement(appartement.identifiant)
            
            result.append(AppartementAvecLocataires(appartement, locataires))
        
        return result
    

def return_to_immeuble(func):
    """
    Decorator used to automatically redirect to the current immeuble page after a POST request.
    Quite usefull to avoid redirection to the immeuble page after each POST request
    """
    @wraps(func)
    async def wrapper(request: Request):
        user = get_current_user_from_cookie(request)
        await func(request)
        return await get_immeuble(request, user)
    return wrapper



@router.get(
    path="/immeubles",
    response_class=HTMLResponse,
    description="Affiche tous les immeubles du client actuel (en fonction de son identifiant)"
)
async def get_immeubles(request: Request,
                        user: Proprietaire = Depends(get_current_user_from_cookie)) -> HTMLResponse:
    
    immeubles = crud_immeubles.get_immeubles_from_proprietaire(user.identifiant)
    
    return templates.TemplateResponse("immeubles.html", {"user": user, "request": request, "immeubles": immeubles})


@router.get(
    "/immeubles/nouveau",
    response_class=HTMLResponse,
    description="Affiche la page de création d'un immeuble. Liée à une requête POST"
)
async def create_immeuble(request: Request,
                          user: Proprietaire = Depends(get_current_user_from_cookie)) -> HTMLResponse:
    
    return templates.TemplateResponse("nouvel_immeuble.html", {"user": user, "request": request})


@router.get(
    "/immeubles/{id}",
    response_class=HTMLResponse,
    description="Affiche les données d'un immeuble indivuduel"
)
async def get_immeuble(request: Request,
                       user: Proprietaire = Depends(get_current_user_from_cookie)) -> HTMLResponse:
    immeuble = crud_immeubles.get_immeuble_from_id(request.path_params["id"])
    
    # Utilisé pour modifier le syndicat d'un immeuble directement depuis la page d'immeuble
    ensemble_syndicats = crud_syndicats.get_all_syndicats(user.identifiant)
    
    syndicat = crud_syndicats.get_syndicat_from_id(immeuble.id_syndicat)
    appartements = AppartementAvecLocataires.from_immeuble(immeuble)
    
    
    return templates.TemplateResponse("immeuble.html", {
        "user": user,
        "request": request,
        "immeuble": immeuble,
        "syndicat": syndicat,
        "appartements": appartements,
        "ensemble_syndicats": ensemble_syndicats
    })
    
    
    

# ---------- POST ----------

    
        
@router.post(
    path="/immeubles/{id}/syndicat/definir",
    response_class=HTMLResponse,
    status_code=201,
    description="Définit le syndicat d'un immeuble"
)
@return_to_immeuble
async def ajouter_syndicat(request: Request):
    FORM = await request.form()
    ID_IMMEUBLE : Final[int] = request.path_params["id"]
    ID_SYNDICAT : Final[int] = FORM.get("syndicat") # type: ignore
    
    return crud_immeubles.ajouter_syndicat_immeuble(ID_IMMEUBLE, ID_SYNDICAT)
        

@router.post(
    path="/immeubles/{id}/syndicat/supprimer",
    response_class=HTMLResponse,
    status_code=201,
    description="Supprime le syndicat d'un immeuble"
)
@return_to_immeuble
async def supprimer_syndicat(request: Request):
    crud_immeubles.reset_syndicat_immeuble(request.path_params["id"])
        


# TODO: Form Appartement 
@router.post(
    "/immeubles/{id}/appartement/ajouter",
    response_class=HTMLResponse, 
    status_code=201,
    description="Ajoute un appartement à un immeuble"
)
@return_to_immeuble
async def ajouter_appartement(request: Request):
    form = await AppartementForm.create(request)
    appartement = form.to_appartement()
    
    exists = crud_appartements.appartement_exists(appartement)
    
    if not exists:
        crud_appartements.add_appartement(appartement)
    
    
    
    

@router.post(
    "/immeubles/nouveau",
    response_class=HTMLResponse,
    description="Ajoute un immeuble à la base de données et redirige vers la page des immeubles"
)
async def create_immeuble_post(request: Request,
                               user: Proprietaire = Depends(get_current_user_from_cookie)):
    immeuble = await create_immeuble_from_form(ImmeubleForm(request), user)
    
    exists = crud_immeubles.immeuble_exists(immeuble, user.identifiant)
    
    if not exists:
        crud_immeubles.add_immeuble(immeuble)
    
    return await get_immeubles(request, user)
        




@router.post(
    "/immeubles/{id}/appartements/{id_appartement}/supprimer",
    response_class=HTMLResponse,
    status_code=201,
    description="Supprime un appartement d'un immeuble"
)
@return_to_immeuble
async def supprimer_appartement(request: Request):
    AppartementCRUD().delete_appartement_from_id(request.path_params["id_appartement"])
        
        