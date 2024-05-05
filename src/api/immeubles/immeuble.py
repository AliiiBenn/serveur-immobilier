from sqlmodel import Field, SQLModel, Relationship


from api.models import Appartement


class Immeuble(SQLModel, table=True):
    identifiant : int = Field(primary_key=True) 
    nom : str 
    adresse : str 
    syndicat : int 
    
    appartements : list["Appartement"] = Relationship(back_populates="immeuble")
    