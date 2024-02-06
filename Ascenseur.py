### Définition de la classe Ascenseur
### @author : Thibault Charlottin
### @contributor : Christine Buisson
from datetime import datetime

class Ascenseur:
    """classe définissant les charactéristiques d'un Ascenseur
    ainsi que les méthodes lui permettant de se déplacer ou d'accueillir des usagers
    """
    def __init__(self, nom, capacite, etages_accessibles, vitesse):
        self.nom = nom #pour utilisation dans les outputs
        self.capacite = capacite #max usagers que peut accueillir, la capa est testée a priori pendant l'appel
        self.etages_accessibles = etages_accessibles #définit la zone d'opération
        self.vitesse = vitesse # en étages/secondes
        self.nombre_personnes = 0 # nombre de personnes présentes dans l'ascenseur
        self.etat = "stationnaire" # non utilisé dans cette version du code
        self.prochains_arret = [] # liste des prochaines missions de l'ascenseur
        self.temps_prochains_arret = [] # liste des heures prochaines missions de l'ascenseur (mêmes indexs que prochains_arrêts)
        self.position = 0 # étage actuel de l'ascenseur
        self.history = {'etage':[0], 'heure':[datetime(year=2019 ,month=4, day=27, hour=7, minute=0, second=0)]} #sauvegarde de l'historique

    def deplacer(self, etage:int):
        """ méthode qui permet de faire déplacer l'ascenseur à un étage donné
        ---
        Inputs :  objet Ascenseur + étage auquel on déplace l'ascenseur
        ---
        Returns : objet Ascenseur updaté à son nouvel étage, modifie l'état de l'ascenseur (non utilisé dans cette version)"""
        self.position = etage
        self.etat = "en_mouvement"
    
    def ajouter_personne(self):
        """ méthode qui permet d'ajouter une personne dans l'ascenseur
        ---
        Inputs :  objet Ascenseur +
        ---
        Returns : update objet Ascenseur en ajoutant 1 à la donnée nombre_personnes"""
        self.nombre_personnes += 1

    def retirer_personne(self):
        """ méthode qui permet de retirer une personne dans l'ascenseur
        ---
        Inputs :  objet Ascenseur +
        ---
        Returns : update objet Ascenseur en retirant 1 à la donnée nombre_personnes"""
        self.nombre_personnes -= 1
