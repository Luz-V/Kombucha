#!/bin/bash

# 1. Installation de Python3 via apt-get
echo "
Installation de python3, venv, pip ...
"
sudo apt-get install -y python3 python3-venv python3-pip

# 2. Création d'un environnement virtuel venv
echo "
Création de l'environnement virtuel et activation..."
python3 -m venv .venv
# Activation de l'environnement virtuel
source .venv/bin/activate

# 3. Installation de flask et d'autres bibliothèques Python via pip
echo "
Installation des bibliothèques Python...
"
# Liste des bibliothèques à installer
libraries=(
    flask
    shapely
    datetime
    geopandas
    fiona
    requests
    PyQt5
    ansi2html  
)
for library in "${libraries[@]}"
do
    pip install "$library"
done

# 4. Fin et désactivation de l'environnement virtuel
echo "
Installation terminée.

Pour exécuter le serveur : 
./run.sh

Pour exécuter le serveur graphique : 
./run_gui.sh

Pour activer manuellement l'environnement virtuel :
. .venv/bin/activate
Pour le désactiver :
deactivate
"
deactivate
