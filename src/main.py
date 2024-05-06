import typing
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from api.engine import Engine 
from api.models import Immeuble
from api.crud import ImmeubleCRUD, CRUD



""" 

POST /login -> se connecter à partir d'un nom, d'un prénom et d'un numéro de téléphone 
POST /signup -> s'inscrire en donnant son nom, son prénom et son numéro de téléphone 

GET /account -> Va afficher le compte de la personne

GET /immeubles/id-immeuble -> va afficher l'immeuble avec cet ID spécifique 
GET /immeubles -> Affiche tous les immeubles de la personne

POST /immeubles -> Ajouter un nouvel immeuble à partir des informations données par l'utilisateur 

GET /immeubles/appartements/id-appartement -> Affiche l'appartement qui possède cet ID spécifique 
POST /immeubles/appartements -> Ajoute un nouvel appartement à partir des informations fournies par l'utilisateur

"""

# app = FastAPI()

# app.mount("/website", StaticFiles(directory="website"), name="website") 

# templates = Jinja2Templates(directory="templates")


# @app.get("/")
# async def root(request: Request):
#     """La page d'accueil est la page où se trouvent la liste d'immeubles et appartements"""
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html"
#     )


# @app.get("/login")
# async def login(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="login.html"
#     )


    

if __name__ == "__main__":
    engine = Engine()
    crud = ImmeubleCRUD(engine)
    
    # crud.create_from_data_without_id("qzd", "Test", 1)
    
    # immeuble = Immeuble(nom="Je suis un message de test", adresse="Test", syndicat=1)
    
    # crud.update_immeuble(1, immeuble)
    crud.delete(1)
