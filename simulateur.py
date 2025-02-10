### Définition de la fonction de simulation
### @author : Thibault Charlottin
### @contributor : Christine Buisson
from Ascenseur import Ascenseur 
from Usager import Usager
from Misc import controle_ascenseur

from datetime import timedelta
import numpy as np

def simuler(evenements_demande, ascenseurs):
    Liste_usagers = []
    for usager in evenements_demande:
         if usager[1] not in Liste_usagers:
            Liste_usagers.append(usager[1])
    while evenements_demande:
        # Sort events by increasing time order
        evenements_demande.sort(key=lambda evenement: evenement[0])
        
        # Process the first event
        evenement = evenements_demande.pop(0)
        temps_actuel = evenement[0]
        if evenement[-1]=='demande':
             # Select the nearest elevator
            Asc = controle_ascenseur(ascenseurs,evenement)
            if type(Asc) != Ascenseur:
                pass
            else :
                # Arrival time of the elevator at the user's floor
                temps_arrivee = temps_actuel + timedelta(seconds = int(np.abs(Asc.position-evenement[1].etage_actuel)/Asc.vitesse))
                temps_attente =  temps_arrivee - temps_actuel
                Asc.temps_prochains_arret = []
                for events in range(len(evenements_demande)):
                    if evenements_demande[events][-1]!='demande' and evenements_demande[events][-2]==Asc:
                        heure = evenements_demande[events][0]+ temps_attente
                        Asc.temps_prochains_arret.append(evenements_demande[events][0])
                        evenements_demande[events] = (heure,evenements_demande[events][1],Asc,evenements_demande[events][-1])
                # Add arrival event for the elevator
                evenements_demande.append((temps_arrivee,evenement[1], Asc, 'devant usager'))
                Asc.prochains_arret.insert(evenement[1].etage_actuel,0)
                Asc.temps_prochains_arret.insert(0,temps_arrivee)

        elif evenement[-1]=='devant usager':
            ascenseur_utilise = evenement[-2]
            ascenseur_utilise.deplacer(evenement[1].etage_actuel)
            ascenseur_utilise.prochains_arret.append(evenement[1].liste_etages[0])
            del(ascenseur_utilise.prochains_arret[0])
            del(ascenseur_utilise.temps_prochains_arret[0])
            ascenseur_utilise.history['etage'].append(ascenseur_utilise.position)
            ascenseur_utilise.history['heure'].append(temps_actuel)
            ascenseur_utilise.ajouter_personne()
            if len(ascenseur_utilise.temps_prochains_arret)==0:
                heure_arrivee_cible = temps_actuel + timedelta(seconds = int(np.abs(evenement[1].etage_actuel-evenement[1].liste_etages[0])/ascenseur_utilise.vitesse))
            else:
                heure_arrivee_cible = max(temps_actuel,ascenseur_utilise.temps_prochains_arret[-1] + timedelta(seconds = int(np.abs(ascenseur_utilise.prochains_arret[-1]-evenement[1].liste_etages[0])/ascenseur_utilise.vitesse)))
            ascenseur_utilise.temps_prochains_arret.append(heure_arrivee_cible)
            evenements_demande.append((heure_arrivee_cible,evenement[1], ascenseur_utilise, 'arrivee a destination'))
            evenement[1].history['heure arrivée ascenseur'].append(temps_actuel)
        elif evenement[-1]== 'arrivee a destination':
            ascenseur_utilise = evenement[-2]
            ascenseur_utilise.deplacer(evenement[1].liste_etages[0])
            evenement[1].etage_actuel = evenement[1].liste_etages[0]
            del(ascenseur_utilise.prochains_arret[0])
            del(ascenseur_utilise.temps_prochains_arret[0])
            del(evenement[1].liste_etages[0])
            ascenseur_utilise.history['etage'].append(ascenseur_utilise.position)
            ascenseur_utilise.history['heure'].append(temps_actuel)
            ascenseur_utilise.retirer_personne()
            evenement[1].history['heures arrivée étage'].append(temps_actuel)
            evenement[1].history['mode transport'].append('Ascenseur')

    return Liste_usagers

