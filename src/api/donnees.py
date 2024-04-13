from dataclasses import dataclass


@dataclass
class Personne:
    nom: str
    prenom: str
    telephone: str


@dataclass
class Syndicat:
    nom: str
    adresse: str
    referent: Personne
    telephone: str
    email: str


@dataclass
class Appartement:
    etage: str
    numero: str
    superficie: str
    personnes : list[Personne]


@dataclass
class Immeuble:
    nom: str
    adresse: str
    syndicat: Syndicat
    appartements: list[Appartement]
