# Kombucha - Formulaire de saisie de donnée

## [En construction]

## Description

Serveur HTTPS minimaliste open source pour la saisie de donnée des structures d'accès au droit. Kombucha fournit les fonctionnalités suivantes :
- Formulaire web : saisie de données par champs pour une personne, un groupe, ou une liste de personnes.
- Vérication de l'appartenance à une zone Quartier Prioritaire de la Ville (QPV) pour une adresse donnée, avec autocomplétion d'adresse postale.
- Enregistrement des données sur serveur au format CSV.
- Partie serveur : Interface graphique utilisateur optionnelle pour activer/désactiver le serveur HTTPS et afficher les logs de connexion.

**Les données traitées par ce formulaire sont anonymisées. Par soucis de respect du RGPD, ce programme n'a pas vocation à traiter des données nominatives**

La vocation de cet projet est de fournir un outil facile à prendre en main pour les aidants numériques, tout en conservant les données en réseau local. 

- Si la procédure d'installation est effectuée intégralement (y compris l'étape ), **toutes les données saisies sont traitées en réseau local par le serveur**.
- Si l'instance Addock n'est pas installée, la vérification des adresses postales nécessite une requête à l'[API Adresse](https://api-adresse.data.gouv.fr/search/) du domaine 'data.gouv.fr'. 

La partie serveur HTTPS fonctionne avec la bibliothèque python [Flask](https://flask.palletsprojects.com) ainsi que quelques outils de traitement géographiques et géométriques ([geopandas](https://geopandas.org), [fiona](https://pypi.org/project/fiona/), [shapely](https://pypi.org/project/shapely/). L'interface web est un simple formulaire en HTML-CSS pourvue de quelques fonctions JavaScript, complétées par un script [jQuery](https://jquery.com/license/). L'interface graphique utilisaeur est construite avec PyQt5. 


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

1. Prérequis : Installation de [Python 3](https://www.python.org/downloads/)

2. Installer les bibliothèques python suivantes (via anaconda, pip ou autre, environnement virtuel conseillé) : `flask, shapely, datetime, geopandas, fiona, requests, PyQt5, ansi2html`


### Optionnel : Création d'une instance addock

L'outil de recherche d'adresse et la base de donnée associée étant libre d'accès, il est possible de rentre autonome le traitement des adresses (autocomplétion + obtention des coordonnées géographiques pour vérification QPV).s

## 2. Utilisation

### Côté serveur

Un serveur HTTPS minimaliste fonctionnant avec la bibliothèque python Flask est


## 3. License
