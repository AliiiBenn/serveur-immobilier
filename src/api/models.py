from typing import Optional
import warnings
from sqlmodel import Field, SQLModel, Relationship





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



