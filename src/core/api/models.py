# from __future__ import annotations

from typing import Optional
import warnings
from sqlmodel import Field, SQLModel, Relationship



""" 

TODO: Ajouter une nouvelle table Compte qui prends en paramètre un email et un mot de passe et qui est relié à une personne. Quand une personne s'inscrit, on crée un compte ET une personne. 

"""



# class Immeuble(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True) 
#     nom : str 
#     adresse : str 
#     syndicat : int 
    
#     appartements : list["Appartement"] = Relationship(back_populates="immeuble")
    
    

# class Appartement(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True)
    
#     etage : int = Field(default=0)
#     numero : int = Field(default=0)
#     superficie : int
    
#     id_immeuble : int | None = Field(default=None, foreign_key="immeuble.identifiant")
#     immeuble : Optional["Immeuble"] = Relationship(back_populates="appartements")
    
#     personnes : list["Personne"] = Relationship(back_populates="appartement")
    
    


# class Compte(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True)
    
#     email : str 
#     mot_de_passe : str
    
#     id_personne : int | None = Field(default=None, foreign_key="personne.identifiant")
#     personne : Optional["Personne"] = Relationship(back_populates="comptes")
    
    
# class Personne(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True)
    
#     nom : str 
#     prenom : str
#     telephone : str
    
#     status : str
    
#     id_appartement : int | None = Field(default=None, foreign_key="appartement.identifiant")
#     appartement : Optional["Appartement"] = Relationship(back_populates="personnes")


# class Syndicat(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True)
    
#     nom : str 
#     adresse : str
#     telephone : str
#     email : str
    
#     referente : int | None = Field(default=None, foreign_key="personne.identifiant")





# class Compte(SQLModel, table=True):
#     identifiant : int = Field(primary_key=True)
    
#     prenom : str
#     nom : str
    
#     email : str
#     mot_de_passe_crypt : str
    
    
    
    
class Personne(SQLModel):
    identifiant : int = Field(primary_key=True)
    
    prenom : str
    nom : str 
    telephone : str
    
    
    
class Proprietaire(Personne, table=True):
    email : str
    mot_de_passe_hash : str
    
    immeubles : list["Immeuble"] = Relationship(back_populates="proprietaire")
    
    
    
# class Locataire(Personne, table=True):
#     id_appartement : int | None = Field(default=None, foreign_key="appartement.identifiant")
#     appartement : Optional["Appartement"] = Relationship(back_populates="locataires")



class Immeuble(SQLModel, table=True):
    identifiant : int = Field(primary_key=True)
    
    nom : str
    adresse : str
    
    id_proprietaire : int = Field(foreign_key="proprietaire.identifiant")
    proprietaire : Optional["Proprietaire"] = Relationship(back_populates="immeubles")
    
