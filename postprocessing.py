import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sns.set_theme('paper')
sns.set_palette('colorblind')

def create_outputs_usagers(Usagers):
    """
    Fonction qui crée un dataframe à partir des historiques des usagers.

    Args:
        Usagers: une liste d'objets Usager

    Returns:
        Un dataframe Pandas contenant les informations des usagers
    """
    histories = [u.history for u in Usagers]
    dataframe_usagers = pd.DataFrame({'usager':[], 'heures demandes':[],'heure arrivée ascenseur': [], 'heures arrivée étage': [], 'mode transport': [], 'etage_demandes':[]})
    for h in range(len(histories)):
        histories[h]['usager'] = [Usagers[h].nom for k in range (4) ]
        dataframe_usagers = pd.concat([dataframe_usagers,pd.DataFrame(histories[h])])
    dataframe_usagers['heures demandes'] = pd.to_datetime(dataframe_usagers['heures demandes'])
    dataframe_usagers['heure arrivée ascenseur'] = pd.to_datetime(dataframe_usagers['heure arrivée ascenseur'])
    dataframe_usagers['heures arrivée étage'] = pd.to_datetime(dataframe_usagers['heures arrivée étage'])
    dataframe_usagers['attente'] = dataframe_usagers['heure arrivée ascenseur']-dataframe_usagers['heures demandes']
    dataframe_usagers['attente'] = dataframe_usagers['attente'].dt.total_seconds()
    dataframe_usagers['temps dans ascenseur'] = dataframe_usagers['heures arrivée étage']-dataframe_usagers['heure arrivée ascenseur']
    dataframe_usagers['temps dans ascenseur'] = dataframe_usagers['temps dans ascenseur'].dt.total_seconds()
    return dataframe_usagers


def create_outputs_ascenseurs(ascenseurs):
    """
    Fonction qui crée un dataframe à partir des historiques des ascenseurs.

    Args:
        ascenseurs: une liste d'objets Ascenseur

    Returns:
        Un dataframe Pandas contenant les informations des ascenseurs
    """
    dataframe_ascenseurs = pd.DataFrame({'Ascenseur': [], 'etage' : [],'heure' :[]})
    for a in ascenseurs:
        a.history['Ascenseur'] = [a.nom for k in range (len(a.history['etage']))]
        dataframe_ascenseurs = pd.concat([dataframe_ascenseurs,pd.DataFrame(a.history)])
    dataframe_ascenseurs['heure'] = pd.to_datetime(dataframe_ascenseurs['heure'])
    return dataframe_ascenseurs

def plot_attente_usagers(Usagers):
    """
    Fonction qui affiche des graphiques sur l'attente des usagers.

    Args:
        Usagers: une liste d'objets Usager

    Returns:
        None
  """
    df_usagers = create_outputs_usagers(Usagers)
    sns.histplot(df_usagers['heures demandes'],kde = True, bins = 100, label = 'heure de demande')
    sns.histplot(df_usagers['heure arrivée ascenseur'],kde = True, bins = 100, label = 'heure arrivée ascenseur')
    sns.histplot(df_usagers['heures arrivée étage'],kde = True, bins = 100, label = 'heure arrivée étage')
    plt.title('Histogramme des demandes, arrivées devant usager et arrivée à destination')
    plt.show()
    df_usagers.sort_values(by='heures demandes', inplace = True)
    df_usagers['plage demande'] = df_usagers['heures demandes'].dt.floor('60T').dt.hour.astype('str')
    sns.boxplot(data = df_usagers, y = 'attente', x='plage demande')
    plt.ylabel('attente [s]')
    plt.xlabel('plage de demande [h]')
    plt.title('Boxplot des attentes par plages d une heure')
    plt.show()
    sns.boxplot(data = df_usagers, y= 'temps dans ascenseur', x = 'plage demande')
    plt.ylabel("temps passé dans l'ascenseur [s]")
    plt.xlabel('plage de demande [h]')
    plt.title('Boxplot des temps de trajet par plages d une heure')
    return 0

def plot_conso_ascenseurs(ascenseurs, facteur_energetique : float):
    """
    Fonction qui affiche la consommation énergétique des ascenseurs.

    Args:
        ascenseurs: une liste d'objets Ascenseur
        facteur_energetique: un float représentant la consommation par étage

    Returns:
        None
    """
    vitesse = ascenseurs[0].vitesse
    dataframe_ascenseurs = create_outputs_ascenseurs(ascenseurs)
    liste_ascenseurs = pd.unique(dataframe_ascenseurs['Ascenseur'])
    conso = [[] for k in range(len(liste_ascenseurs)) ]
    for k in range (len(liste_ascenseurs)):
        df = dataframe_ascenseurs[dataframe_ascenseurs['Ascenseur']==liste_ascenseurs[k]]
        df.sort_values(by='heure')
        for e in range(1,len(df['etage'])):
            conso[k].append(np.abs(df['etage'][e-1]-df['etage'][e])*(facteur_energetique/vitesse))
        conso[k].insert(0,0)
    for c in range(len(conso)) : 
        plt.scatter(liste_ascenseurs[c],np.sum(conso[c]))
    plt.ylabel('consomation totale [kWh]')
    plt.xlabel('Ascenseur')
    plt.title('Consomation par ascenseur')
    return 0
