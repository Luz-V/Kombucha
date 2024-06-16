# Kombucha - Formulaire de saisie de donnée
## [En construction]
## Introduction
## 1. Installation
### Sous Debian
1. Cloner le dépot ou télécharger les fichiers. Par exemple, dans votre dossier utilisateur.

2. Se placer dans le répertoire Kombucha et exécuter le script d'installation `install.sh` (droits admins requis pour l'utilisation d'apt). En supposant que le dépot est situé dans **~/Kombucha** : 
```
cd ~/Kombucha
./install.sh
```

Ce script vérifie via `apt` l'installation de `python3, python3-venv, python3-pip` ainsi que les bibliothèques requises au fonctionnement du serveur. Une fois la vérification terminée, un environnement virtuel python venv est crée dans un sous-dossier **/.venv** à la racine du répertoire de travail. 

Un fois l'exécution du script terminée, le serveur est prêt à être lancé à l'aide des scripts `run.sh` ou `run_gui.sh` (voir [Utilisation](#2-utilisation)).

### Autres (Fedora, Windows, MacOS)

1. Pré-requis : Installation de [Python 3](https://www.python.org/downloads/)

2. Installer les bibliothèques python suivantes (via anaconda, pip ou autre, environnement virtuel conseillé) : `flask, shapely, datetime, geopandas, fiona, requests, PyQt5, ansi2html`

## 2. Utilisation



## 3. License
