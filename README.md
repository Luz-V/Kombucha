![License](https://img.shields.io/github/license/Luz-V/Kombucha)

<h1>Kombucha</h1>

<img align="left" width="100" height="100" src="https://github.com/Luz-V/Kombucha/blob/main/static/icon4.png"> 

Formulaire de saisie web et serveur HTTP minimaliste open source pour la saisie de données des équipes d'accès aux droits. Projet utilisé en point d'accès aux droits dans un centre social parisien.

![Exemple de formulaire](/static/example.png)

## Sommaire

1. [Présentation](#1-présentation)
2. [Installation](#2-installation)
3. [Utilisation](#3-utilisation)
4. [Licence](#4-licence)


## 1. Présentation
Kombucha propose les fonctionnalités suivantes :
- Formulaire web : saisie de données par champs pour une personne, une liste de personne, ou un groupe.
- Vérification de l'appartenance à une zone Quartier Prioritaire de la politique de la Ville (QPV) pour une adresse postale donnée, avec autocomplétion.
- Enregistrement des données sur serveur au format CSV.
- Interface graphique utilisateur pour activer/désactiver le serveur HTTP et afficher les logs de connexion côté serveur.

La vocation de ce projet est de fournir un outil facile à prendre en main pour les aidants numériques, tout en conservant les données saisie en réseau local pour s'assurer de leur protection. 

⚠️ Les données traitées par ce formulaire sont **anonymisées**. Par soucis de respect du RGPD, ce programme n'a **pas vocation à traiter des données nominatives**.

Si la procédure d'installation est effectuée intégralement (y compris l'[étape optionnelle](#optionnel--création-dune-instance-adock)), toutes les données saisies seront **traitées en réseau local** par le serveur. Sinon, la vérification des adresses postales nécessitera une requête à l'[API Adresse](https://adresse.data.gouv.fr/api-doc/adresse) du domaine data.gouv.fr. Il s'agit alors de la seule requête web effectuée lors de la saisie.

Coté client, l'interface web est un modeste formulaire HTML/CSS assorti de quelques fonctions JavaScript complétées par un script [jQuery](https://jquery.com/license/) pour l'autocomplétion. 
La partie serveur HTTP fonctionne avec la bibliothèque python [Flask](https://flask.palletsprojects.com) adossée aux outils de traitement géographique [fiona](https://pypi.org/project/fiona/) et [geopandas](https://geopandas.org), ainsi que la bibliothèque de géométrie [shapely](https://pypi.org/project/shapely/).

La recherche d'adresse fait appel à l'[API Adresse](https://api-adresse.data.gouv.fr/search/) du gouvernement français, dont une instance peut être hébergée localement via docker (avec la liste de toutes les adresses de France), ou de manière distante en utilisant celle disponible à l'adresse [api-adresse.data.gouv.fr/search/](https://api-adresse.data.gouv.fr/search/). 
Deux bases de données du gouvernement français sont utilisées :
- [Base Adresse Nationale](https://adresse.data.gouv.fr/donnees-nationales)
- [Quartiers Prioritaires de la politique de la ville (QPV)](https://www.data.gouv.fr/fr/datasets/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/)

 L'interface graphique utilisateur du serveur est construite avec [PyQt5](https://pypi.org/project/PyQt5/). 


## 2. Installation

### Debian/Ubuntu

1. Cloner le dépot ou télécharger les fichiers. Par exemple, dans votre dossier utilisateur.

2. Se placer dans le répertoire Kombucha et exécuter le script d'installation `install.sh` (droits admins requis pour l'utilisation d'apt). En supposant que le dépot est cloné dans **~/Kombucha** : 
```
cd ~/Kombucha
./install.sh
```

Ce script vérifie via `apt` l'installation de `python3, python3-venv, python3-pip` ainsi que les bibliothèques requises au fonctionnement du serveur. Une fois la vérification terminée, un environnement virtuel python **venv** est crée dans un sous-dossier **/.venv** à la racine du répertoire de travail. 

Un fois l'exécution du script terminée, le serveur est prêt à être lancé à l'aide des scripts `run.sh` ou `run_gui.sh` (voir [Utilisation](#3-utilisation)).

### Autres (Fedora, Windows, MacOS)

1. Prérequis : Installation de [Python 3](https://www.python.org/downloads/)

2. Installer les bibliothèques python suivantes (via anaconda, pip ou autre, environnement virtuel conseillé) : `flask, shapely, datetime, geopandas, fiona, requests, PyQt5, ansi2html`


### Optionnel : Création d'une instance adock

L'outil de recherche d'adresse et la base de donnée associée étant en accès libre, il est possible d'effectuer localement le traitement des adresses (autocomplétion + obtention des coordonnées géographiques pour vérification QPV). Pour cela, environ **2,5 Go d'espace disque** sont nécessaires sur serveur pour télécharger la base Adresse Nationale complète et faire tourner une instance de l'API nécessaire à la recherche locale d'adresse.

La procédure détaillée est décrite ici : [Installer une instance avec les données de la base adresse nationale](https://github.com/BaseAdresseNationale/addok-docker#installer-une-instance-avec-les-donn%C3%A9es-de-la-base-adresse-nationale)

Une fois l'installation terminée, la variable du booléen **adock_running** déclarée en début du fichier `Kombucha_server.py` doit être modifiée directement dans le code comme égale à `True` :
```
# Booléen indicateur de l'installation + lancement d'instance Adock
adock_running = True
```

⚠️ Ce choix implique une **mise à jour annuelle** de la Base Adresse Nationale. Mais il en va de toute façon de même pour les données géographiques QPV.


## 3. Utilisation

### Côté serveur

Sous Debian, l'activation de l'environnement python et le lancement de `Kombucha_server.py` se fait simplement via le script `run.sh` :
```
cd ~/Kombucha
./run.sh
```

De même l'interface de contrôle graphique peut être utilisée à la place via `run_gui.sh` : 
```
cd ~/Kombucha
./run_gui.sh
```

Lors du lancement du serveur (via le terminal ou l'interface de contrôle), Flask indique dans un message d'en-tête l'adresse http du serveur à communiquer aux clients. L'exemple ci-dessous est extrait des logs Flask :
```
 * Serving Flask app 'Kombucha_server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.200.201:5000
Press CTRL+C to quit
```
Dans l'exemple ci-dessus : 
- l'adresse `http://127.0.0.1:5000` peut être utilisée pour ouvrir le formulaire web depuis le serveur.
- l'adresse `http://192.168.200.201:5000` peut être utilisée pour ouvrir le formulaire web depuis les autres clients en réseau local.

⚠️ En l'absence de configuration supplémentaire, le serveur n'est **pas accessible à un poste distant (hors réseau local)**. Pour des raisons de sécurité, une telle configuration **est déconseillée** par principe, le but de ce projet restant de fournir un outil local et non distant.

### Côté client

Une fois le serveur lancé, les postes sur le même réseau local que le serveur peuvent se connecter directement au formulaire via navigateur web pour commencer la saisie de donnée. Dans l'exemple précédent, il s'agirait de l'adresse `http://192.168.200.201:5000` à indiquer dans le navigateur. Aucune installation n'est requise côté client, l'adresse http suffit.

Trois formulaires sont implémentés :
- Un premier formulaire individuel accessible depuis l'adresse principale 
- Un formulaire multiple pour une liste d'individus, accessible à l'adresse **/massive** - soit, en reprenant l'exemple précédent, `http://192.168.200.201:5000/massive`
- Un formulaire de groupe pour une entrée collective, accessible à l'adresse **/group** - soit, en reprenant l'exemple précédent, `http://192.168.200.201:5000/group`

## 4. Licence

Le contenu original proposé dans ce dépot est sous licence MIT. Il est utilisable et modifiable librement, sous condition d'inclure la licence d'origine. La licence complète est [disponible ici](https://github.com/Luz-V/Kombucha/blob/main/LICENSE). Cette licence n'inclut pas les contenus non originaux open source déjà sous licence utilisés dans ce projet, dont voici une liste que j'espère la plus exhaustive possible :
- [Python](https://docs.python.org/3/license.html)
- [pip](https://github.com/pypa/pip/blob/main/LICENSE.txt)
- [Virtualenv](https://github.com/pypa/virtualenv/blob/main/LICENSE) 
- [API Adresse + Base Adresse Nationale + Données QPV](https://github.com/etalab/licence-ouverte/blob/master/LO.md)
- [Flask](https://flask.palletsprojects.com/en/2.3.x/license/)
- [PyQt5](https://doc.qt.io/qtforpython-6/licenses.html)
- [jQuery](https://jquery.com/license/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Fiona](https://github.com/Toblerity/Fiona?tab=BSD-3-Clause-1-ov-file)
- [Geopandas](https://github.com/geopandas/geopandas/blob/main/LICENSE.txt)
- [Shapely](https://github.com/shapely/shapely/blob/main/LICENSE.txt)
- [ansi2html](https://github.com/pycontribs/ansi2html/blob/main/LICENSE)
- [Pathlib](https://github.com/chigopher/pathlib/blob/master/LICENSE)



