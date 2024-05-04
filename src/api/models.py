from typing import Self
from sqlmodel import Field, SQLModel, Session, create_engine

from api.engine import Engine



class Immeuble(SQLModel, table=True):
    identifiant : int = Field(primary_key=True) 
    nom : str 
    adresse : str 
    syndicat : int 
    # TODO: Ajouter la liste d'appartements
    
    
    

# engine = create_engine(
#     "sqlite:///database/main.db",
#     echo=True
# )


# SQLModel.metadata.create_all(engine) 

# with Session(engine) as session:
#     session.add(
#         Immeuble(
#             identifiant=1,
#             nom="Test",
#             adresse="He",
#             syndicat=2
#         )
#     )
    
#     session.commit()


