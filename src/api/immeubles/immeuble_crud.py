
import warnings

from sqlmodel import Session

from api.immeubles.immeuble import Immeuble
from api.engine import Engine



class ImmeubleCRUD:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        
        
    def create(self, immeuble : Immeuble) -> Immeuble:
        with Session(self.engine.engine) as session:
            session.add(immeuble)
            session.commit()
            
            return immeuble
        
        
    def create_from_data(self, identifiant: int, nom: str, adresse: str, syndicat: int) -> Immeuble:
        immeuble = Immeuble(identifiant=identifiant, nom=nom, adresse=adresse, syndicat=syndicat)
        
        return self.create(immeuble)
        
        
    def create_without_id(self, nom: str, adresse: str, syndicat: int) -> Immeuble:
        immeuble = Immeuble(nom=nom, adresse=adresse, syndicat=syndicat)
        
        return self.create(immeuble)
        
            
            
    def read(self, identifiant: int) -> Immeuble | None:
        with Session(self.engine.engine) as session:
            immeuble = session.get(Immeuble, identifiant)
            session.commit()
            
            return immeuble
        





    
    
    
    
if __name__ == '__main__':
    warnings.warn("This is a module, not a script. It is not meant to be run directly.")
    
    engine = Engine()
    
    crud = ImmeubleCRUD(engine)
    
    # crud.create_without_id("Immeuble", "Adresse", 1)
    
    with Session(engine.engine) as session:
        immeuble = session.get(Immeuble, 1)
        print(immeuble)
    
    