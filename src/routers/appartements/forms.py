from typing import Optional

from dataclasses import dataclass

from fastapi import Request

from core.api.models import Appartement



@dataclass 
class AppartementForm:
    etage : str 
    numero : str
    surface : str
    loyer : str
    id_immeuble : str
    
    def to_appartement(self) -> Appartement:
        return Appartement(
            etage=self.etage,
            numero=self.numero,
            surface=self.surface,
            loyer=self.loyer,
            id_immeuble=self.id_immeuble
        )
    
    @classmethod
    async def create(cls, request : Request) -> "AppartementForm":
        form = await request.form()
        
        return cls(
            etage=form.get("etage"), # type: ignore
            numero=form.get("numero"), # type: ignore
            surface=form.get("surface"), # type: ignore
            loyer=form.get("loyer"), # type: ignore
            id_immeuble=request.path_params["id"]
        )
        