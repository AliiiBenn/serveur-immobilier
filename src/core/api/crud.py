from typing import Sequence, overload
from fastapi import Request
from sqlmodel import Session, select
from .models import Appartement, Immeuble, Locataire, Proprietaire, Syndicat
from .engine import Engine



engine = Engine()





class ImmeubleCRUD:
    def get_immeuble_from_id(self, id : int) -> Immeuble | None:
        """Retourne l'immeuble avec l'identifiant id"""
        with Session(engine.engine) as session:
            immeuble = session.exec(select(Immeuble).where(Immeuble.identifiant == id))
            
            return immeuble.first()
        
        
    def get_immeuble_from_name_and_adresse(self, nom : str, adresse : str) -> Immeuble | None:
        """Retourne l'immeuble avec le nom et l'adresse donnés"""
        with Session(engine.engine) as session:
            immeuble = session.exec(
                select(Immeuble).where(Immeuble.nom == nom).where(Immeuble.adresse == adresse)
            )
        
            
            return immeuble.first()
        
        
    def get_immeuble_from_request(self, request: Request) -> Immeuble:
        """Retourne l'immeuble avec l'identifiant donné dans le path"""
        return self.get_immeuble_from_id(request.path_params["id"])
    
    
    def get_immeubles_from_proprietaire(self, idenfifiant_proprietaire: int) -> Sequence[Immeuble]:
        """Retourne la liste des immeubles du propriétaire donné"""
        with Session(engine.engine) as session:
            immeubles = session.exec(select(Immeuble).where(Immeuble.id_proprietaire == idenfifiant_proprietaire)).all()
            return immeubles
        
        
    def ajouter_syndicat_immeuble(self, id_immeuble : int, id_syndicat : int) -> None:
        """Définit le syndicat d'un immeuble"""
        with Session(engine.engine) as session:
            immeuble = self.get_immeuble_from_id(id_immeuble)
            
            if immeuble is None:
                raise ValueError(f"Un immeuble avec l'identifiant {id_immeuble} n'existe pas")
            
            immeuble.id_syndicat = id_syndicat
            session.add(immeuble)
            session.commit()
            session.refresh(immeuble)
            
            
    def add_immeuble(self, immeuble : Immeuble) -> None:
        """Ajoute une immeuble à la base de données"""
        with Session(engine.engine) as session:
            session.add(immeuble)
            session.commit()
        
        
    def reset_syndicat_immeuble(self, id_immeuble) -> None:
        """Réinitialise le syndicat d'une immeuble"""
        with Session(engine.engine) as session:
            immeuble = self.get_immeuble_from_id(id_immeuble)
            
            if immeuble is None:
                raise ValueError(f"Un immeuble avec l'identifiant {id_immeuble} n'existe pas")
            
            immeuble.id_syndicat = None
            session.add(immeuble)
            session.commit()
            session.refresh(immeuble)
        
        
    def immeuble_exists(self, immeuble : Immeuble, identifiant_proprietaire : str) -> bool:
        """Vérifie si une immeuble existe dans la base de données"""
        with Session(engine.engine) as session:
            immeuble = session.exec(
                select(Immeuble).where(Immeuble.nom == immeuble.nom).where(Immeuble.adresse == immeuble.adresse)\
                                .where(Immeuble.id_proprietaire == identifiant_proprietaire)
            )
            
            return immeuble.first() is not None
    
    
    
class SyndicatCRUD:
    def get_syndicat_from_id(self, id : int | None) -> Syndicat | None:
        """Retourne le syndicat avec l'identifiant donné"""
        with Session(engine.engine) as session:
            syndicat = session.exec(select(Syndicat).where(Syndicat.identifiant == id))
            
            return syndicat.first()
        
        
    def get_syndicat_from_name_and_adresse(self, nom : str, adresse : str) -> Syndicat | None:
        """Retourne le syndicat avec le nom et l'adresse donnés"""
        with Session(engine.engine) as session:
            syndicat = session.exec(
                select(Syndicat).where(Syndicat.nom == nom).where(Syndicat.adresse == adresse)
            )
            
            return syndicat.first()
        
    def get_all_syndicats(self, identifiant_proprietaire : int) -> Sequence[Syndicat]:
        """Retourne la liste des syndicats du propriétaire donné"""
        with Session(engine.engine) as session:
            syndicats = session.exec(select(Syndicat).where(Syndicat.id_referente == identifiant_proprietaire)).all()
            return syndicats
        
        
    def syndicat_exists(self, syndicat : Syndicat, identifiant_proprietaire : str) -> bool:
        """Vérifie si un syndicat existe dans la base de données"""
        with Session(engine.engine) as session:
            syndicat = session.exec(
                select(Syndicat).where(Syndicat.nom == syndicat.nom).where(Syndicat.adresse == syndicat.adresse)\
                                .where(Syndicat.telephone == syndicat.telephone).where(Syndicat.email == syndicat.email)\
                                .where(Syndicat.id_referente == identifiant_proprietaire)
            )
            
            return syndicat.first() is not None
        

    def get_immeubles_of_syndicat(self, syndicat: Syndicat) -> Sequence[Immeuble]:
        """Retourne la liste des immeubles du syndicat donné"""
        with Session(engine.engine) as session:
            return session.exec(select(Immeuble).where(Immeuble.id_syndicat == syndicat.identifiant)).all()
        
    
    def add_syndicat(self, syndicat : Syndicat) -> None:
        """Ajoute un syndicat à la base de données"""
        with Session(engine.engine) as session:
            session.add(syndicat)
            session.commit()
        
      
        
class LocataireCRUD:
    def get_locataires_from_appartement(self, id_appartement: int) -> Sequence[Locataire]:
        """Retourne la liste des locataires d'un appartement donné"""
        with Session(engine.engine) as session:
            locataires = session.exec(select(Locataire).where(Locataire.id_appartement == id_appartement)).all()
            return locataires
        
        
    def get_locataire_from_id(self, id : int) -> Locataire | None:
        """Retourne l'appartement avec l'identifiant donné"""
        with Session(engine.engine) as session:
            locataire = session.exec(select(Locataire).where(Locataire.identifiant == id))
            
            return locataire.first()
        
        
    def locataire_exists(self, locataire : Locataire, id_appartement : int) -> bool:
        """Vérifie si un locataire existe dans la base de données"""
        with Session(engine.engine) as session:
            locataire = session.exec(
                select(Locataire).where(Locataire.prenom == locataire.prenom)\
                                 .where(Locataire.nom == locataire.nom)\
                                 .where(Locataire.telephone == locataire.telephone)\
                                 .where(Locataire.id_appartement == id_appartement)
            )
            
            return locataire.first() is not None
        
        
        
    def add_locataire(self, locataire : Locataire) -> None:
        """Ajoute un locataire à la base de données"""
        with Session(engine.engine) as session:
            session.add(locataire)
            session.commit()
            session.refresh(locataire)
            
            
    def delete_locataire_from_id(self, id : int) -> None:
        """Supprime l'appartement avec l'identifiant donné"""
        with Session(engine.engine) as session:
            locataire = self.get_locataire_from_id(id)
            
            if locataire is None:
                raise ValueError(f"Un locataire avec l'identifiant {id} n'existe pas")
            
            session.delete(locataire)
            session.commit()
            
            
            
  
class AppartementCRUD:
    def get_appartements_from_immeuble(self, id_immeuble: int) -> Sequence[Appartement]:
        """Retourne la liste des appartements d'un immeuble donné"""
        with Session(engine.engine) as session:
            appartements = session.exec(select(Appartement).where(Appartement.id_immeuble == id_immeuble)).all()
            return appartements
        
        
    def get_appartement_from_id(self, id : int) -> Appartement | None:
        """Retourne l'appartement avec l'identifiant donné"""
        with Session(engine.engine) as session:
            appartement = session.exec(select(Appartement).where(Appartement.identifiant == id))
            
            return appartement.first()
        
            
    def get_appartement_from_request_path(self, request : Request) -> Appartement:
        """Retourne l'appartement avec l'identifiant donné dans le path"""
        return self.get_appartement_from_id(request.path_params["id_appartement"])
        
        
    def get_locataire_from_id(self, id : int) -> Locataire | None:
        """Retourne l'appartement avec l'identifiant donné"""
        with Session(engine.engine) as session:
            locataire = session.exec(select(Locataire).where(Locataire.identifiant == id))
            
            return locataire.first()
            
            
    def delete_appartement_from_id(self, id : int) -> None:
        """Supprime l'appartement avec l'identifiant donné"""
        with Session(engine.engine) as session:
            appartement = self.get_appartement_from_id(id)
            
            if appartement is None:
                raise ValueError(f"Un appartement avec l'identifiant {id} n'existe pas")
            
            locataires = LocataireCRUD().get_locataires_from_appartement(id)
            
            for locataire in locataires:
                session.delete(locataire)
            
            session.delete(appartement)
            session.commit()
            
            
    def add_appartement(self, appartement : Appartement) -> None:
        """Ajoute un appartement à la base de données"""
        with Session(engine.engine) as session:
            session.add(appartement)
            session.commit()
            
            
    def appartement_exists(self, appartement : Appartement) -> bool:
        """Vérifie si un appartement existe dans la base de données"""
        with Session(engine.engine) as session:
            appartement = session.exec(select(Appartement)\
                        .where(Appartement.etage == appartement.etage)\
                        .where(Appartement.numero == appartement.numero)\
                        .where(Appartement.id_immeuble == appartement.id_immeuble)
            )
        
            
            return appartement.first() is not None
        
        
    def get_all_appartements(self, id_immeuble : int) -> Sequence[Appartement]:
        """Retourne la liste des appartements d'un immeuble donné"""
        with Session(engine.engine) as session:
            appartements = session.exec(select(Appartement).where(Appartement.id_immeuble == id_immeuble)).all()
            return appartements
        
        
        
    