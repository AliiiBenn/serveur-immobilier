from dataclasses import dataclass
from typing import Optional

from fastapi import Request


@dataclass
class SyndicatForm:
    request : Request
    
    nom : Optional[str] = None
    adresse : Optional[str] = None
    telephone : Optional[str] = None
    email : Optional[str] = None
    
    def __post_init__(self):
        self.errors = []
        
        
    async def load_data(self) -> None:
        form = await self.request.form()
        
        self.nom = form.get("name") # type: ignore
        self.adresse = form.get("address") # type: ignore
        self.telephone = form.get("telephone") # type: ignore
        self.email = form.get("email") # type: ignore
        
    
    async def validate(self) -> bool:
        if not self.nom:
            self.errors.append("Le nom du syndicat est obligatoire")
        
        if not self.adresse:
            self.errors.append("L'adresse du syndicat est obligatoire")
            
        if not self.telephone:
            self.errors.append("Le numéro de téléphone du syndicat est obligatoire")
            
        if not self.email:
            self.errors.append("L'email du syndicat est obligatoire")
            
        if not self.errors:
            return True
        return False