from dataclasses import dataclass, field

from fastapi import Request

from core.api.models import Immeuble, Proprietaire





@dataclass
class ImmeubleForm:
    request : Request
    
    nom : str | None = field(default=None)
    adresse : str | None = field(default=None)
    
    def __post_init__(self):
        self.errors = []
        
        self.is_loaded = False
        

    
    
    async def load_data(self) -> None:
        form = await self.request.form()
        
        self.nom = form.get("name") # type: ignore
        self.adresse = form.get("address") # type: ignore
        
        self.is_loaded = True
        
    
    async def validate(self) -> bool:
        if not self.nom:
            self.errors.append("Le nom de l'immeuble est obligatoire")
        
        if not self.adresse:
            self.errors.append("L'adresse de l'immeuble est obligatoire")
            
        if not self.errors:
            return True
        return False
    
    

async def create_immeuble_from_form(form : ImmeubleForm, user : Proprietaire) -> Immeuble | None:
    if not form.is_loaded:
        await form.load_data()
        
    if not await form.validate():
        return None
    
    
    immeuble = Immeuble(
        nom=form.nom,
        adresse=form.adresse,
        id_proprietaire=user.identifiant
    )
    
    return immeuble




    
    
    