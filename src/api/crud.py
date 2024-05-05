from sqlmodel import Session
from api.models import Immeuble, Appartement, Personne, Syndicat
from api.engine import Engine


from typing import Final, Protocol, TypeVar


T = TypeVar("T")


class CRUD(Protocol[T]):
    engine : Engine
    
    def create(self, obj : T) -> None:
        ...
    
    def read(self, id : int) -> T:
        ...
    
    def update(self, obj : T) -> None:
        ...
    
    def delete(self, id : int) -> None:
        ...



""" 

What should it do for better interface ?

- Create with a an `Immeuble` object
- Create only with an immeuble data 
- Create with immeuble data without id

"""
class ImmeubleCRUD(CRUD[Immeuble]):
    """Base class used to manipulate `Immeuble` table with a CRUD behavior"""
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        
        
    @property 
    def engine(self) -> Engine:
        return self.__engine.engine
    
    
    def create(self, immeuble : Immeuble) -> None:
        with Session(self.engine) as session:
            session.add(immeuble)
            session.commit()
            
            
    def create_from_data(self, identifiant : str, nom : str, adresse : str, syndicat : int) -> None:
        immeuble = Immeuble(identifiant=identifiant, nom=nom, adresse=adresse, syndicat=syndicat)
        self.create(immeuble)
        
        
    def create_from_data_without_id(self, nom : str, adresse : str, syndicat : int) -> None:
        immeuble = Immeuble(nom=nom, adresse=adresse, syndicat=syndicat)
        self.create(immeuble)
            
            
    def read(self, id : int) -> Immeuble:
        with Session(self.engine) as session:
            return session.exec(Immeuble).get(id)
    
    
    def update(self, immeuble : Immeuble) -> None:
        with Session(self.engine) as session:
            session.add(immeuble)
            session.commit()
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            session.delete(session.exec(Immeuble).get(id))
            session.commit()
            
            
            
            
class AppartementCRUD(CRUD[Appartement]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        

    
    
    def create(self, appartement : Appartement) -> None:
        with Session(self.engine) as session:
            session.add(appartement)
            session.commit()
            
            
    def read(self, id : int) -> Appartement:
        with Session(self.engine) as session:
            return session.exec(Appartement).get(id)
    
    
    def update(self, appartement : Appartement) -> None:
        with Session(self.engine) as session:
            session.add(appartement)
            session.commit()
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            session.delete(session.exec(Appartement).get(id))
            session.commit()
            
            
            
            
            
class PersonneCRUD(CRUD[Personne]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine

    
    
    def create(self, personne : Personne) -> None:
        with Session(self.engine) as session:
            session.add(personne)
            session.commit()
            
            
    def read(self, id : int) -> Personne:
        with Session(self.engine) as session:
            return session.exec(Personne).get(id)
        
        
    def update(self, personne : Personne) -> None:
        with Session(self.engine) as session:
            session.add(personne)
            session.commit()
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            session.delete(session.exec(Personne).get(id))
            session.commit()
            
            
            
            
            
class SyndicatCRUD(CRUD[Syndicat]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
    
    
    def create(self, syndicat : Syndicat) -> None:
        with Session(self.engine) as session:
            session.add(syndicat)
            session.commit()
            
            
    def read(self, id : int) -> Syndicat:
        with Session(self.engine) as session:
            return session.exec(Syndicat).get(id)
    
    
    def update(self, syndicat : Syndicat) -> None:
        with Session(self.engine) as session:
            session.add(syndicat)
            session.commit()
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            session.delete(session.exec(Syndicat).get(id))
            session.commit()