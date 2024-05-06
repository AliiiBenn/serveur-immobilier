from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError


from api.models import Immeuble, Appartement, Personne, Syndicat, Compte
from api.engine import Engine

from typing import Final, Protocol, TypeVar



T = TypeVar("T")


class CRUD(Protocol[T]):
    engine : Engine
    
    def create(self, obj : T) -> None:
        ...
    
    def read(self, id : int) -> T:
        ...
    
    def update(self, id : int, obj : T) -> None:
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
        
        
        
class ImmeubleNotFoundError(ValueError):
    def __init__(self, message : str) -> None:
        super().__init__(message)
        
        


class ImmeubleCRUD(CRUD[Immeuble]):
    """Base class used to manipulate `Immeuble` table with a CRUD behavior"""
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        
        
    @property 
    def engine(self) -> Engine:
        return self.__engine.engine
    
    
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
            
            
    def read(self, id : int) -> Immeuble | None:
        with Session(self.engine) as session:
            # return session.get(Immeuble, id)
            immeuble = session.exec(select(Immeuble).where(Immeuble.identifiant == id))
            
            return immeuble.first()
        
        
    def read_from_name_and_adresse(self, nom : str, adresse : str) -> Immeuble | None:
        with Session(self.engine) as session:
            immeuble = session.exec(
                select(Immeuble).where(Immeuble.nom == nom).where(Immeuble.adresse == adresse)
            )
            
            return immeuble.first()
        
    
            
    # TODO: Add a new method to update the immeuble with an immeuble as parameter
    def update(self, id : int, new_immeuble : Immeuble) -> None:
        with Session(self.engine) as session:
            current_immeuble = self.read(id)
            
            if current_immeuble is None:
                raise ImmeubleNotFoundError(f"An immeuble with the id {id} does not exist")
            
            current_immeuble.nom = new_immeuble.nom
            current_immeuble.adresse = new_immeuble.adresse
            current_immeuble.syndicat = new_immeuble.syndicat
            
            session.add(current_immeuble)
            session.commit()
            session.refresh(current_immeuble)
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            immeuble = self.read(id)
            
            if immeuble is None:
                raise ImmeubleNotFoundError(f"An immeuble with the id {id} does not exist")
            
            session.delete(immeuble)
            session.commit()
            
            
class AppartementNotFoundError(ValueError):
    def __init__(self, message : str) -> None:
        super().__init__(message)
            
            
class AppartementCRUD(CRUD[Appartement]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        

    @property
    def engine(self) -> Engine:
        return self.__engine.engine
    
    
    def create(self, appartement : Appartement) -> None:
        with Session(self.engine) as session:
            session.add(appartement)
            session.commit()
            
            
    def read(self, id : int) -> Appartement | None:
        with Session(self.engine) as session:
            appartement = session.exec(select(Appartement).where(Appartement.identifiant == id))
            
            return appartement.first()
        
        
    def update(self, id : int, appartement : Appartement) -> None:
        with Session(self.engine) as session:
            current_appartement = self.read(id)
            
            if current_appartement is None:
                raise AppartementNotFoundError(f"An appartement with the id {id} does not exist")
            
            current_appartement.etage = appartement.etage
            current_appartement.numero = appartement.numero
            current_appartement.superficie = appartement.superficie
            
            session.add(current_appartement)
            session.commit()
            session.refresh(current_appartement)
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            current_appartement = self.read(id)
            
            if current_appartement is None:
                raise AppartementNotFoundError(f"An appartement with the id {id} does not exist")
            
            session.delete(current_appartement)
            session.commit()
            
            
        

class PersonneNotFoundError(ValueError):
    def __init__(self, message : str) -> None:
        super().__init__(message)
            
            
class PersonneCRUD(CRUD[Personne]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        
        
    @property
    def engine(self) -> Engine:
        return self.__engine.engine

    
    
    def create(self, personne : Personne) -> None:
        with Session(self.engine) as session:
            session.add(personne)
            session.commit()
            
            
    def read(self, id : int) -> Personne | None:
        with Session(self.engine) as session:
            personne = session.exec(Personne).get(id)
            
            return personne 
        
        
        
        
    def update(self, id : int,personne : Personne) -> None:
        with Session(self.engine) as session:
            current_personne = self.read(id)
            
            if current_personne is None:
                raise PersonneNotFoundError(f"A personne with the id {id} does not exist")
            
            
            current_personne.nom = personne.nom
            current_personne.prenom = personne.prenom
            current_personne.telephone = personne.telephone
            
            session.add(current_personne)
            session.commit()
            session.refresh(current_personne)
            
            
    def delete(self, id : int) -> None:
        with Session(self.engine) as session:
            personne = self.read(id)
            
            if personne is None:
                raise PersonneNotFoundError(f"A personne with the id {id} does not exist")
            
            session.delete(personne)
            session.commit()
            
            

class SyndicatNotFoundError(ValueError):
    def __init__(self, message : str) -> None:
        super().__init__(message)

            
            
class SyndicatCRUD(CRUD[Syndicat]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
    
    
    @property
    def engine(self) -> Engine:
        return self.__engine.engine
    
    
    def create(self, syndicat : Syndicat) -> None:
        with Session(self.engine) as session:
            session.add(syndicat)
            session.commit()
            
            
    def read(self, id : int) -> Syndicat | None:
        with Session(self.engine) as session:
            syndicat = session.exec(select(Syndicat).where(Syndicat.identifiant == id))
            
            return syndicat.first()
        
        
    def update(self, id : int, syndicat : Syndicat) -> None:
        with Session(self.engine) as session:
            current_syndicat = self.read(id)
            
            if current_syndicat is None:
                raise SyndicatNotFoundError(f"A syndicat with the id {id} does not exist")
            
            current_syndicat.nom = syndicat.nom
            current_syndicat.adresse = syndicat.adresse
            current_syndicat.telephone = syndicat.telephone
            current_syndicat.email = syndicat.email
            
            session.add(current_syndicat)
            session.commit()
            session.refresh(current_syndicat)
            
            
    def delete(self, id : int) -> None: 
        with Session(self.engine) as session:
            current_syndicat = self.read(id)
            
            if current_syndicat is None:
                raise SyndicatNotFoundError(f"A syndicat with the id {id} does not exist")
            
            session.delete(current_syndicat)
            
            
            
            
class CompteNotFoundError(ValueError):
    def __init__(self, message : str) -> None:
        super().__init__(message)
        
        
class CompteCRUD(CRUD[Compte]):
    def __init__(self, engine : Engine) -> None:
        self.__engine = engine
        
        
    @property
    def engine(self) -> Engine:
        return self.__engine.engine
    
    
    def create(self, compte : Compte) -> None:
        with Session(self.engine) as session:
            session.add(compte)
            session.commit()
            
            
    def read(self, id : int) -> Compte | None:
        with Session(self.engine) as session:
            compte = session.exec(select(Compte).where(Compte.identifiant == id))
            
            return compte.first()
        
        
    def update(self, id : int, compte : Compte) -> None:
        with Session(self.engine) as session:
            current_compte = self.read(id)
            
            if current_compte is None:
                raise CompteNotFoundError(f"A compte with the id {id} does not exist")
            
            current_compte.email = compte.email
            current_compte.mot_de_passe = compte.mot_de_passe
            
            session.add(current_compte)
            session.commit()
            session.refresh(current_compte)
            
            
    def delete(self, id : int) -> None: 
        with Session(self.engine) as session:
            current_compte = self.read(id)
            
            if current_compte is None:
                raise CompteNotFoundError(f"A compte with the id {id} does not exist")
            
            session.delete(current_compte)