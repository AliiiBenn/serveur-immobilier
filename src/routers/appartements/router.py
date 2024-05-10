from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from core.api.auth import get_current_user_from_cookie

from core.api.models import Locataire
from core.api.crud import ImmeubleCRUD, AppartementCRUD, LocataireCRUD
from core.api.engine import Engine

engine = Engine()


router = APIRouter()
templates = Jinja2Templates(directory="../templates")


    
async def create_locataire_from_request_form(request : Request) -> Locataire:  
    form = await request.form()
    prenom = form.get("prenom")
    nom = form.get("nom")
    telephone = form.get("telephone")
    email = form.get("email")
    
    return Locataire(
        prenom=prenom,
        nom=nom,
        telephone=telephone,
        email=email if email is not None else None,
    )
    
    
def redirect_to_appartement(id_immeuble : int, id_appartement : int) -> RedirectResponse:
    return RedirectResponse(f"/immeubles/{id_immeuble}/appartements/{id_appartement}",
                            status_code=status.HTTP_302_FOUND)
    
    
    
async def add_locataire_from_request_form(request : Request) -> None:
    locataire = await create_locataire_from_request_form(request)
    locataire.id_appartement = request.path_params["id_appartement"]
    
    if not LocataireCRUD().locataire_exists(locataire, request.path_params["id_appartement"]):
        LocataireCRUD().add_locataire(locataire)
    


@router.get(
    path="/immeubles/{id}/appartements/{id_appartement}",
    response_class=HTMLResponse,
    description="Affiche les données d'un appartement indivuduel"
)
async def get_appartement(request: Request, user: str = Depends(get_current_user_from_cookie)):
    immeuble = ImmeubleCRUD().get_immeuble_from_id(request.path_params["id"])
    appartement = AppartementCRUD().get_appartement_from_id(request.path_params["id_appartement"])
    locataires = LocataireCRUD().get_locataires_from_appartement(appartement.identifiant)
    
    
    context = {
        "request": request,
        "user": user,
        "immeuble": immeuble,
        "appartement": appartement,
        "locataires": locataires
    }
    
    return templates.TemplateResponse("appartement.html", context)
    
    
    


    
@router.post(
    path="/immeubles/{id}/appartements/{id_appartement}/resident/ajouter",
    response_class=RedirectResponse,
    status_code=201,
    description="Ajoute un locataire à un appartement"
)
async def ajouter_resident(request: Request,
                           user: str = Depends(get_current_user_from_cookie),
                           ) -> RedirectResponse:
    
    await add_locataire_from_request_form(request)
    
    return redirect_to_appartement(request.path_params["id"], request.path_params["id_appartement"])

    

    
    
@router.post(
    path="/immeubles/{id}/appartements/{id_appartement}/resident/{id_locataire}/supprimer",
    response_class=HTMLResponse,
    status_code=201,
    description="Supprime un locataire d'un appartement"
)
async def supprimer_resident(request: Request, user: str = Depends(get_current_user_from_cookie)):
    LocataireCRUD().delete_locataire_from_id(request.path_params["id_locataire"])
        
        
    return redirect_to_appartement(request.path_params["id"], request.path_params["id_appartement"])




@router.post(
    "/immeubles/{id}/appartements/{id_appartement}/modifier",
    response_class=RedirectResponse,
    status_code=201,
    description="Modifie les données d'un appartement"
)
async def modifier_appartement(request: Request, user: str = Depends(get_current_user_from_cookie)):
    form = await request.form()
    etage = form.get("etage")
    numero = form.get("numero")
    surface = form.get("surface")
    loyer = form.get("loyer")
    
    with Session(engine.engine) as session:
        appartement = AppartementCRUD().get_appartement_from_id(request.path_params["id_appartement"])
        
        if len(etage): # type: ignore
            appartement.etage = etage
        if len(numero): # type: ignore
            appartement.numero = numero
        if len(surface): # type: ignore
            appartement.surface = surface
        if len(loyer): # type: ignore
            appartement.loyer = loyer
        
        session.add(appartement)
        session.commit()
        
    return redirect_to_appartement(request.path_params["id"], request.path_params["id_appartement"])