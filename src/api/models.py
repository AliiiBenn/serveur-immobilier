from typing import Final, Literal, Optional, Self, TYPE_CHECKING
import warnings
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

TESTING : Final[bool] = False


from api.engine import Engine

if TYPE_CHECKING:
    from api.immeubles.immeuble import Immeuble

# class Immeuble(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True) 
#     nom : str 
#     adresse : str 
#     syndicat : int 
    
#     appartements : list["Appartement"] = Relationship(back_populates="immeuble")
    
    

class Appartement(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    etage : int = Field(default=0)
    numero : int = Field(default=0)
    superficie : int
    
    id_immeuble : int | None = Field(default=None, foreign_key="immeuble.identifiant")
    immeuble : Optional["Immeuble"] = Relationship(back_populates="appartements")
    
    personnes : list["Personne"] = Relationship(back_populates="appartement")
    
    
class Personne(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    nom : str 
    prenom : str
    telephone : str
    
    status : str
    
    id_appartement : int | None = Field(default=None, foreign_key="appartement.identifiant")
    appartement : Optional["Appartement"] = Relationship(back_populates="personnes")


class Syndicat(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    nom : str 
    adresse : str
    telephone : str
    email : str
    
    referente : int | None = Field(default=None, foreign_key="personne.identifiant")



if __name__ == '__main__':
    warnings.warn("This is a module, not a script. It is not meant to be run directly.")
    
    engine = Engine()
    
    SQLModel.metadata.create_all(engine.engine)
    
    # with Session(engine.engine) as session:
    #     immeuble = Immeuble(
    #         identifiant=2,
    #         nom="Immeuble",
    #         adresse="Adresse",
    #         syndicat=1
    #     )
        
    #     appartement = Appartement(identifiant=1, superficie=134, immeuble=immeuble)
    #     appartement2 = Appartement(identifiant=2, superficie=134, immeuble=immeuble)
        
        
    #     appartement.immeuble = immeuble
    #     appartement2.immeuble = immeuble
        
    #     session.add(appartement)
    #     session.add(appartement2)
        
    #     print(immeuble.appartements)
        
    #     session.commit()
    
    

