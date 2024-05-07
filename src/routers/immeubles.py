from dataclasses import dataclass, field
from typing import Sequence, TypeAlias
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from core.api.auth import get_current_user_from_cookie

from fastapi import Depends, Request, APIRouter
from fastapi.templating import Jinja2Templates


from core.api.models import Proprietaire, Immeuble
from core.api.auth import get_current_user_from_cookie
from core.api.engine import Engine


router = APIRouter()
templates = Jinja2Templates(directory="../templates")
engine = Engine()


@dataclass
class ImmeubleForm:
    request : Request
    
    nom : str | None = field(default=None)
    adresse : str | None = field(default=None)
    
    def __post_init__(self):
        self.errors = []
        

    
    
    async def load_data(self) -> None:
        form = await self.request.form()
        
        self.nom = form.get("name") # type: ignore
        self.adresse = form.get("address") # type: ignore
        
    
    async def validate(self) -> bool:
        if not self.nom:
            self.errors.append("Le nom de l'immeuble est obligatoire")
        
        if not self.adresse:
            self.errors.append("L'adresse de l'immeuble est obligatoire")
            
        if not self.errors:
            return True
        return False
    
    



@router.get("/immeubles", response_class=HTMLResponse)
async def get_immeubles(request: Request, user: Proprietaire = Depends(get_current_user_from_cookie)) -> HTMLResponse:
    print(immeubles := await get_immeubles(user.identifiant))
    
    return templates.TemplateResponse("immeubles.html", {"user": user, "request": request, "immeubles": immeubles})


@router.get("/immeubles/nouveau", response_class=HTMLResponse)
async def create_immeuble(request: Request, user: Proprietaire = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("nouvel_immeuble.html", {"user": user, "request": request})




@router.post("/immeubles/nouveau", response_class=HTMLResponse)
async def create_immeuble(request: Request, user: Proprietaire = Depends(get_current_user_from_cookie)):
    form = ImmeubleForm(request)
    await form.load_data()
    
    if await form.validate():
        with Session(engine.engine) as session:
            immeuble = Immeuble(
                nom=form.nom,
                adresse=form.adresse,
                id_proprietaire=user.identifiant
            )
            
            print(immeuble)
            
            session.add(immeuble)
            session.commit()
        
    
    return await get_immeubles(request, user)




async def get_immeubles(idenfifiant_proprietaire: str) -> Sequence[Immeuble]:
    with Session(engine.engine) as session:
        immeubles = session.exec(select(Immeuble).where(Immeuble.id_proprietaire == idenfifiant_proprietaire)).all()
        return immeubles
    