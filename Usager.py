# Définition de la classe Usager
### @author : Thibault Charlottin
### @contributor : Christine Buisson


class Usager:
    """Définition de la classe Usager qui ne possède pas de méthodes, cest une coquille vide"""
    def __init__(self, liste_etages, heures_demandes, facteur_impatience,nom):
        self.liste_etages = liste_etages # liste des étages que l'usager doit atteindre au cours de sa journée
        self.heures_demandes = heures_demandes # liste des heures auxquelles l'usager appellera l'ascenseur 
        self.facteur_impatience = facteur_impatience # POUR AJOUT ESCALIERS : facteur qui influe la décision de prendre l'escalier
        self.nom = nom # nom de l'usager, pour création des outputs
        self.etage_actuel = 0 # étage auquel se situe l'usager
        self.history = {'heures demandes': heures_demandes,'heure arrivée ascenseur': [], 'heures arrivée étage': [], 'mode transport': [], 'etage_demandes': liste_etages.copy()} # historique de l'usager, pour utilisation dans les outputs


