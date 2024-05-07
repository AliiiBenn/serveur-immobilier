# serveur-immobilier




POST /login -> se connecter à partir d'un nom, d'un prénom et d'un numéro de téléphone 
POST /signup -> s'inscrire en donnant son nom, son prénom et son numéro de téléphone 

GET /account -> Va afficher le compte de la personne

GET /immeubles/id-immeuble -> va afficher l'immeuble avec cet ID spécifique 
GET /immeubles -> Affiche tous les immeubles de la personne

POST /immeubles -> Ajouter un nouvel immeuble à partir des informations données par l'utilisateur 

GET /immeubles/appartements/id-appartement -> Affiche l'appartement qui possède cet ID spécifique 
POST /immeubles/appartements -> Ajoute un nouvel appartement à partir des informations fournies par l'utilisateur
