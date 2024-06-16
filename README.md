# | <img src="https://github.com/Luz-V/Kombucha/blob/main/static/icon4.png" width="48"> | Kombucha |
Formulaire de saisie web pour l'accès aux droits :
![Exemple de formulaire](/static/example.png)

## Description

Serveur HTTP minimaliste et open source pour la saisie de données des équipes d'accès aux droits. Kombucha propose les fonctionnalités suivantes :
- Formulaire web : saisie de données par champs pour une personne, un groupe, ou une liste de personnes.
- Vérication de l'appartenance à une zone Quartier Prioritaire de la Ville (QPV) pour une adresse postale donnée, avec autocomplétion.
- Enregistrement des données sur serveur au format CSV.
- Interface graphique utilisateur pour activer/désactiver le serveur HTTPS et afficher les logs de connexion côté serveur.

La vocation de cet projet est de fournir un outil facile à prendre en main pour les aidants numériques, tout en conservant les données saisie en réseau local pour s'assurer de leur protection. 

⚠️ Les données traitées par ce formulaire sont **anonymisées**. Par soucis de respect du RGPD, ce programme n'a **pas vocation à traiter des données nominatives**.

Si la procédure d'installation est effectuée intégralement (y compris l'[étape optionnelle](#optionnel--création-dune-instance-adock)), toutes les données saisies seront **traitées en réseau local** par le serveur. Sinon, la vérification des adresses postales nécessitera une requête à l'[API Adresse](https://api-adresse.data.gouv.fr/search/) du domaine data.gouv.fr. Il s'agit alors de la seule requête web effectuée lors de la saisie.

Coté client, l'interface web est un modeste formulaire HTML/CSS assorti de quelques fonctions JavaScript complétées par un script [jQuery](https://jquery.com/license/) pour l'autocomplétion. 
La partie serveur HTTPS fonctionne avec la bibliothèque python [Flask](https://flask.palletsprojects.com) adossés à quelques outils de traitement géographiques et géométriques [fiona](https://pypi.org/project/fiona/), [shapely](https://pypi.org/project/shapely/).

La recherche d'adresse fait appel à l'[API Adresse](https://api-adresse.data.gouv.fr/search/) du gouvernement français, qui peut être hébergé localement via docker, ou en utilisant l'instance disponible à l'adresse [api-adresse.data.gouv.fr/search/](https://api-adresse.data.gouv.fr/search/). 
Deux bases de données du gouvernement français sont utilisées :
- [Base Adresse Nationale](https://adresse.data.gouv.fr/donnees-nationales)
- [Quartiers Prioritaires de la politique de la ville (QPV)](https://www.data.gouv.fr/fr/datasets/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/)

 L'interface graphique utilisateur du serveur est construite avec [PyQt5](https://pypi.org/project/PyQt5/). 


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


### Optionnel : Création d'une instance adock

L'outil de recherche d'adresse et la base de donnée associée étant libre d'accès, il est possible de rentre autonome le traitement des adresses (autocomplétion + obtention des coordonnées géographiques pour vérification QPV).s

## 2. Utilisation

### Côté serveur

Un serveur HTTPS minimaliste fonctionnant avec la bibliothèque python Flask est


## 3. License
