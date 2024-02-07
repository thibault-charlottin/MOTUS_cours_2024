## MOTUS 2024 : Simulation des déplacement au sein de la tour Séquoia sur une journée

Copyrights:<br>
@Author : Thibault Charlottin <br>
@Contributor : Christine Buisson <br>

## Installation des packages

2 options sont possibles à vous :<br>
- après avoir installé conda, ouvrir Anaconda navigator puis cliquer sur invite de commandes depuis le navigateur :

Copy your local path to this repository
Then open the command prompt
```bash
cd %paste your path
```

````bash
conda env create -f conda/env.yaml
````

Activate it:
````bash
conda activate motus
````

You can then run the commands in the console.ipynb file 

### Windows installation
Copy your local path to this repository
Open Anaconda navigator
Open CMD.exe prompt and type
````bash
cd %paste your path
````

then type 
````bash
conda env create -f env.yml
````

Activate it:
````bash
conda activate motus
````
- Option 2 : passer par la fenêtre environnement de Anaconda Navigator comme présenté en cours

Vous pouvez alors lancer le code depuis le fichier Console.ipynb
__________________________________________________________________
## Achitecture du code
```
📦ACC platoon fuel consumption
 ┣ 📂conda
 ┃ ┣ 📜env.yaml
 ┣ 📜Ascenseur.py %contient la classe Ascenseur
 ┣ 📜Misc.py %contient la génération de la demande et le système de contrôle de l'ascenseur
 ┣ 📜postprocessing.py %fonctions de plot
 ┣ 📜Usager.py %contient la classe Usager
 ┣ 📜simulateur.py %fonction de simulation du modèle
 ┗ 📜Console.ipynb %interface que vous utilisez pour générer les codes
```
 Merci de respecter cette architecture quand vous coderez et de bien conserver le formalisme que nous avons mis en place pour les commentaires
