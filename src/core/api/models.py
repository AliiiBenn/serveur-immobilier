from __future__ import annotations

from typing import Optional
import warnings
from sqlmodel import Field, SQLModel, Relationship



""" 

TODO: Ajouter une nouvelle table Compte qui prends en paramètre un email et un mot de passe et qui est relié à une personne. Quand une personne s'inscrit, on crée un compte ET une personne. 

"""




    
    
class Personne(SQLModel):
    identifiant : int = Field(primary_key=True)
    
    prenom : str
    nom : str 
    telephone : str
    
    
    
    
    
class Proprietaire(Personne, table=True):
    email : str
    mot_de_passe_hash : str
    
    # immeubles : list["Immeuble"] = Relationship(back_populates="proprietaire") immeubles
    # syndicats : list["Syndicat"] = Relationship(back_populates="referente")
    
    
    
class Locataire(Personne, table=True):
    email : Optional[str] = Field(default=None)
    
    id_appartement : int | None = Field(default=None, foreign_key="appartement.identifiant")
    
    
    # appartement : Optional["Appartement"] = Relationship(back_populates="locataires")



class Immeuble(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    nom : str
    adresse : str
    
    id_proprietaire : int = Field(foreign_key="proprietaire.identifiant")
    # proprietaire : Optional["Proprietaire"] = Relationship(back_populates="immeubles")
    
    id_syndicat : int | None = Field(default=None, foreign_key="syndicat.identifiant")
    # syndicat : Optional["Syndicat"] = Relationship(back_populates="immeubles")
    
    # appartements : list["Appartement"] = Relationship(back_populates="immeuble")


class Syndicat(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    nom : str 
    adresse : str
    
    telephone : str
    email : str
    
    id_referente : int = Field(foreign_key="proprietaire.identifiant")
    # referente : Optional["Proprietaire"] = Relationship(back_populates="syndicats")
    
    # immeubles : list["Immeuble"] = Relationship(back_populates="syndicat")
    
    
    
    
class Appartement(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    etage : int
    numero : int
    surface : int
    
    loyer : int
    
    id_immeuble : int = Field(foreign_key="immeuble.identifiant")
    # immeuble : Optional["Immeuble"] = Relationship(back_populates="appartements")
    
    # personnes : list["Personne"] = Relationship(back_populates="appartement")