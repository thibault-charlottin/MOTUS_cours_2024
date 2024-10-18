#fonction utilitaires pour le simulateur d'ascenseur
### @author : Thibault Charlottin
### @contributor : Christine Buisson
from datetime import datetime, timedelta
import scipy.stats as stats
import numpy as np
from Usager import Usager



def convertir_heures_timestamp(heures_decimales:float):
    """
    Fonction pour convertir un nombre décimal représentant des heures en un timestamp.
    Args:
        heures_decimales: Un nombre décimal représentant des heures.
    Returns:
        Un objet datetime représentant le timestamp.
    """
    # Déterminer le nombre d'heures
    heures = int(heures_decimales)
    # Déterminer le nombre de minutes
    minutes = int((heures_decimales - heures) * 60)
    # Déterminer le nombre de secondes
    secondes = int(((heures_decimales - heures) * 60 - minutes) * 60)
    return datetime(year=2019 ,month=4, day=27, hour=heures, minute=minutes, second=secondes)



# Fonction qui affecte des valeurs binaires en fonction d'une probabilité donnée
def affectation (proba):
    if random.random() < proba:
        return 1
    else :
        return 0




# Définition de la fonction de génération des événements de demande
def generer_evenements_demande(nombre_usagers : int, debut_arrivee_employes : int, fin_arrivee_employes : int,
                            debut_pause_dejeuner : int, fin_pause_dejeuner : int,
                            duree_mini_pause_dejeuner : int, duree_max_pause_dejeuner : int,
                            debut_depart_employes : int, fin_depart_employes : int,                          valeur_graine : int, proba : float):
    
    """génère la demande de l'ascenseur pour chaque usager
    ---
    Chaque heure de demande est le résultat d'une loi normale tronquée par des heures de début et de fin.
    Chaque étage de demande est le résultat d'une loi uniforme sur l'ensemble des étages. 
    On attribue un étage de travail par usager. 
    ---
    Inputs : 
    - nombre_usagers : nombre d'utilisateurs à générer
    - debut_arrivee_employes : heure des premières arrivées au travail
    - fin_arrivee_employes : heure des dernières arrivées au travail
    - debut_pause_dejeuner : heure des premiers départs pour le réfectoire/l'extérieur le midi
    - fin_pause_dejeuner : heure des derniers départs pour le réfectoire/l'extérieur le midi
    - duree_mini_pause_dejeuner : durée mini de la pause déjeuner
    - duree_max_pause_dejeuner : durée max de la pause déjeuner
    - debut_depart_employes : heure des premiers départs du travail
    - fin_depart_employes : heure des derniers départs du travail
    - valeur_graine : valeur que l'on donne à la graine aléatoire pour assurer que les résultats des tirages aléatoires 
    soient identiques d'un tirage à un autre
    ---
    Outputs : 
    evenements_demande : liste des évènements de demande, liste de tuples contenant
    (heure de la demande, Usager instancié, typologie d'évènement (uniquement demande ici))"""
    
    rng = np.random.RandomState(valeur_graine)

    evenements_demande = []
    #génération des moyennes et écarts types des lois normales
    #rien ne vous empêche de les modifier mais soyez cohérents sur les heures que vous utilisez en bornes
    moyenne_arrivee = (fin_arrivee_employes + debut_arrivee_employes) / 2
    ecart_type_arrivee = (fin_arrivee_employes - debut_arrivee_employes) / 4
    
    moyenne_dejeuner = (fin_pause_dejeuner + debut_pause_dejeuner) / 2
    ecart_type_dejeuner = (fin_pause_dejeuner- debut_pause_dejeuner) / 4

    duree_moyenne_dejeuner = (duree_max_pause_dejeuner + duree_mini_pause_dejeuner) / 2
    ecart_type_duree_dejeuner = (duree_max_pause_dejeuner - duree_mini_pause_dejeuner) / 4

    moyenne_depart = (fin_depart_employes + debut_depart_employes) / 2
    ecart_type_depart = (fin_depart_employes- debut_depart_employes) / 4
    
    
    # Liste qui servira à affecter utilisation escalier (1) ou acsenseur (0) à un utilisateur
    choix=[]


    for i in range(nombre_usagers):
        # Heure d'arrivée de l'usager
        heure_arrivee_sur_site = stats.truncnorm((debut_arrivee_employes-moyenne_arrivee)/ecart_type_arrivee,
                                                  (fin_arrivee_employes-moyenne_arrivee)/ecart_type_arrivee, loc=moyenne_arrivee, scale=ecart_type_arrivee).rvs(random_state=rng)
        # Heure de déjeuner de l'usager
        heure_dejeuner = stats.truncnorm((debut_pause_dejeuner-moyenne_dejeuner)/ecart_type_dejeuner,
                                                  (fin_pause_dejeuner-moyenne_dejeuner)/ecart_type_dejeuner, loc=moyenne_dejeuner, scale=ecart_type_dejeuner).rvs(random_state=rng)
        # Heure de retour au bureau de l'usager

        heure_retour_bureau = heure_dejeuner + stats.truncnorm((duree_mini_pause_dejeuner-duree_moyenne_dejeuner)/ecart_type_duree_dejeuner,
                                                  (duree_max_pause_dejeuner-duree_moyenne_dejeuner)/ecart_type_duree_dejeuner, loc=duree_moyenne_dejeuner, scale=ecart_type_duree_dejeuner).rvs(random_state=rng)
        # Heure de départ de l'usager
        heure_depart = stats.truncnorm((debut_depart_employes-moyenne_depart)/ecart_type_depart,
                                                  (fin_depart_employes-moyenne_depart)/ecart_type_depart, loc=moyenne_depart, scale=ecart_type_arrivee).rvs(random_state=rng)
        # Conversion des floats obtenus en output des lois normales en format datetime
        heures_demande = [convertir_heures_timestamp(heure_arrivee_sur_site),
                          convertir_heures_timestamp(heure_dejeuner),
                          convertir_heures_timestamp(heure_retour_bureau),
                          convertir_heures_timestamp(heure_depart)]
        etage_de_travail = np.random.randint(0, 35) #le 36e etage c'est celui du ministre rêve pas t'y auras pas accès 
        liste_etages = [etage_de_travail,0,etage_de_travail,0]
        # Facteur d'impatience de l'usager
        facteur_impatience = np.random.uniform(0, 1)
        #instantiation de l'usager
        usager = Usager(liste_etages, heures_demande, facteur_impatience,i)
        #ajout des évènements de demande dans la liste de sortie de la fonction
        for h in heures_demande:
            choix.append(affectation(proba))
            if etage_de_travail < 4 and choix[-1]==1:
                evenements_demande.append((h, usager, 'demande_escalier'))
            else :
                evenements_demande.append((h, usager, 'demande_acsenseur'))
        evenements_demande.sort(key=lambda evenement: evenement[0])
    return evenements_demande


def controle_ascenseur(liste_ascenseurs:list,evenement:tuple):
    """Fonction qui détermine quel ascenseur se déplace vers l'usager qui vient de faire sa demande
    ---
    Trois scénarios sont possibles :
    - il existe un ou des ascenseurs vides, dans ce cas c'est l'ascenseur vide le plus proche qui vient
    - il existe un ou des ascenseurs occupés mais à moins qu'à la capacité qui passent par l'endroit de la demande,
      dans ce cas c'est l'ascenseur le plus proche qui s'arrêtera et cet arrêt devient le premier de la liste
    - aucun ascenseur n'est disponible, on regénère un évènement de demande pour l'usager 10 secondes plus tard
    ---
    inputs :
    - liste_ascenseurs : liste des objets ascenseurs
    - evenement : évènement de demande de l'usager
    ---
    output : 
    - ascenseur si un ascenseur est sélectionné
    - evenement_out : nouvel évènement de demande"""
    ascenseurs_libres = []
    ascenseurs_possibles = []
    for asc in liste_ascenseurs:
        if asc.nombre_personnes<asc.capacite and int(evenement[1].liste_etages[0]) in asc.etages_accessibles and int(evenement[1].etage_actuel) in asc.etages_accessibles:
            if asc.prochains_arret==[]:
                ascenseurs_libres.append(asc)
            elif  asc.position<=int(evenement[1].liste_etages[0])<=asc.prochains_arret[0] or asc.position>=int(evenement[1].liste_etages[0])>=asc.prochains_arret[0]:
                ascenseurs_possibles.append(asc)
    if len(ascenseurs_libres)>0: #cas 1 un ascenseur est vide
        positions = [np.abs(a.position-evenement[1].etage_actuel) for a in ascenseurs_libres]
        ascenseur = ascenseurs_libres[positions.index(min(positions))]
        return ascenseur
    elif len(ascenseurs_possibles)>0 : #cas 2, un ascenseur passe par l'étage au cours de sa course
        positions = [np.abs(a.position-evenement[1].etage_actuel) for a in ascenseurs_possibles]
        ascenseur = ascenseurs_possibles[positions.index(min(positions))]
        return ascenseur
    else : 
        heure = evenement[0] + timedelta(seconds =10)
        evenement_out = (heure,evenement[1],evenement[2])
        return evenement_out
