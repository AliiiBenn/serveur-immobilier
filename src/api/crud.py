from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError


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


- Custom errors 

"""

class ImmeubleWithIDAlreadyExistsError(ValueError):
    def __init__(self, message : str, immeuble : Immeuble) -> None:
        super().__init__(message)
        self.immeuble = immeuble
        
        
        
class ImmeubleWithNameAndAdresseAlreadyExistsError(ValueError):
    def __init__(self, message : str, immeuble : Immeuble) -> None:
        super().__init__(message)
        self.immeuble = immeuble


class ImmeubleCRUD(CRUD[Immeuble]):
    """Base class used to manipulate `Immeuble` table with a CRUD behavior"""
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        
        
    @property 
    def engine(self) -> Engine:
        return self.__engine.engine
    
    
    # TODO: Check if an immeuble with the same name and adresse already exists
    def create(self, immeuble : Immeuble) -> None:
        """Create a new immeuble and append it to the database

        Args:
            immeuble (`Immeuble`): The immeuble to create

        Raises:
            `ImmeubleAlreadyExistsError`: In case an immeuble with the ID already exists

        It is pretty simple to use this method. Here's an example:
        
        ```python
        immeuble = Immeuble(identifiant=1, nom="Test", adresse="test", syndicat=1) # Create a new immeuble object
        crud.create(immeuble)
        ```

        """
        def already_exists(nom : str, adresse : str) -> bool:
            """Local function to check if an immeuble with the same name and adresse already exists"""
            return self.read_from_name_and_adresse(nom, adresse) is not None
        
        
        try:
            if already_exists(immeuble.nom, immeuble.adresse):
                raise ImmeubleWithNameAndAdresseAlreadyExistsError(
                    "An immeuble with the same name and adresse already exists",
                    immeuble
                )
            
            with Session(self.engine) as session:
                session.add(immeuble)
                session.commit()
        except IntegrityError as e:
            e.add_note(f"The id of the immeuble that already exists is {immeuble.identifiant}")
            
            raise ImmeubleWithIDAlreadyExistsError(
                f"An immeuble with the same id already exists",
                immeuble
            ) from e
            
            
    def create_from_data(self, identifiant : int, nom : str, adresse : str, syndicat : int) -> None:
        immeuble = Immeuble(identifiant=identifiant, nom=nom, adresse=adresse, syndicat=syndicat)
        self.create(immeuble)
        
        
    def create_from_data_without_id(self, nom : str, adresse : str, syndicat : int) -> None:
        immeuble = Immeuble(nom=nom, adresse=adresse, syndicat=syndicat)
        self.create(immeuble)
            
            
    def read(self, id : int) -> Immeuble:
        with Session(self.engine) as session:
            return session.get(Immeuble, id)
        
        
    def read_from_name_and_adresse(self, nom : str, adresse : str) -> Immeuble:
        with Session(self.engine) as session:
            immeuble = session.exec(
                select(Immeuble).where(Immeuble.nom == nom).where(Immeuble.adresse == adresse)
            )
            
            return immeuble.first()
        
    
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