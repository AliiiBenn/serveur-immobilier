from typing import Self
import warnings
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from engine import Engine



class Immeuble(SQLModel, table=True):
    identifiant : int = Field(primary_key=True) 
    nom : str 
    adresse : str 
    syndicat : int 
    
    appartements : list["Appartement"] = Relationship(back_populates="immeuble")
    
    

class Appartement(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    etage : int = Field(default=0)
    numero : int = Field(default=0)
    superficie : int
    
    immeuble : "Immeuble" = Relationship(back_populates="appartements")
    
    # TODO: Liste de personnes liées à l'appartement
    
    





if __name__ == '__main__':
    warnings.warn("This is a module, not a script. It is not meant to be run directly.")
    
    engine = Engine()
    
    SQLModel.metadata.create_all(engine.engine)
    
    appa = Appartement(identifiant=1)
    
    

