# Kombucha - Formulaire de saisie de donnée
## [En construction]
## Introduction
## 1. Installation
### Sous Debian
1. Cloner le dépot ou télécharger les fichiers

2. Se placer dans le répertoire de travail et exécuter le script d'installation `install.sh` (droits admins requis lors de l'utilisation d'apt).

Ce script vérifie l'installation de python3, python3-venv, python3-pip ainsi que les bibliothèques requises au fonctionnement du serveur. Une fois la vérification terminée, un environnement virtuel python venv est crée dans un sous dossier `.venv` à la racine du répertoire de travail. 

Un fois l'exécution du script terminée, le serveur est prêt à être lancé à l'aide des scripts `run.sh` ou `run_gui.sh` (voir [Utilisation](/Utilisation))

Liste des bibliothèques python installées par le script d'installation : flask, shapely, datetime, geopandas, fiona, requests, PyQt5, ansi2html

### Autres (Fedora, Windows, MacOS)

1. Pré-requis : Installation de python3

2. Installer les bibliothèques python suivantes (via anaconda, pip ou autre, environnement virtuel conseillé)
- flask
- shapely
- datetime
- geopandas
- fiona
- requests
- PyQt5
- ansi2html

## 2. Utilisation



## 3. License
