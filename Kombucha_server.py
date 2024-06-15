from flask import Flask, render_template, request, jsonify, url_for
from shapely.geometry import Point
from datetime import date as dt
from geopandas import read_file
from fiona import listlayers
from sys import argv
import requests
import csv


###### Serveur web minimaliste pour la gestion de requêtes en local d'un formulaire HTML

###### Utilise le framework Flask, ainsi que d'autres bibliothèques python tel que Geopandas et Fiona
###### La rechercher et autocomplétion d'adresse fait appel à l'API Adresse du gouvernement français et le script jQuery v3.6.0 ( (c) OpenJS Foundation)

###### INSTALLATION SERVEUR : voir Script d'installation

###### Pour effectuer l'autocomplétion d'adresse en local, une instance Addok est requise : 
###### => https://github.com/BaseAdresseNationale/addok-docker#installer-une-instance-avec-les-donn%C3%A9es-de-la-base-adresse-nationale
###### => Données QPV officielles : https://www.data.gouv.fr/fr/datasets/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/

###### Il est vivement conseillé d'utiliser un gestionnaire environnement virtuel comme venv pour l'installation des dépendances python. L'installation d'Addok indiquée ci-dessus se fait via docker.   

###### Lancement de l'application sur machine : flask --app formulaire_mix run
###### Lancement de l'application en réseau local : flask --app formulaire run_mix --host=0.0.0.0


###### INSTALLATION CLIENT : 
###### Aucune installation requise. Accès par navigateur HTTP aux adresses : 
# http://$adresse_serveur:5000/
# http://$adresse_serveur:5000/group
# http://$adresse_serveur:5000/massive


##### Fonctions et variables globales

##### Chemin vers le fichier gpkg utilisé pour les QPV
### Partie à mettre à jour en cas de modifications des données QPV
# Ici, nous avons adaptés ce fichier gpkg pour distinguer 3 types de QPV : QPV Amandiers, QPV porte 20ème, et autres QPV.
fichier_gpkg = "/home/lucvedie/projet_formulaire/QPV_split_WGS84.gpkg"

##### Chemin vers le fichier d'export des données
### A mettre à jour en fonction de l'arborsecence système
filename = "/home/lucvedie/projet_formulaire/data.csv"
### Fin de partie à mettre à jour


##### Application Flask 
app = Flask(__name__)        

# Variable pour contrôler l'état de l'application Flask
flask_running = False

##### Formulaire principal
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # Date actuelle au format ISO (AAAA-MM-JJ)
    today_date = dt.today().isoformat()  
    
    # Requête POST : Récupération des données du formulaire
    if request.method == 'POST':
        date = request.form['date']
        genre = request.form['genre']
        age = request.form['age']
        provenance = request.form['provenance']
        code_postal = request.form.get('code_postal') 
        qpv = request.form['qpv']
        type_logement = request.form['type_logement']
        foyer = request.form['foyer']
        bailleur_social = request.form['bailleur_social']
        autre_logement = request.form['precisez']
        objet_demande = request.form['objet_demande']
        commentaire = request.form['commentaire']
        
        # Indique les cases à cocher "traitement en interne" et "personne redirigée"
        interne_amandiers = "X" if request.form.get('interne_amandiers') else ""
        redirigee = "X" if request.form.get('redirigee') else ""
         
        # Remplace la provenance par le code postal s'il est choisi
        if provenance == "Autre code postal" and code_postal:
            provenance = code_postal
        # Remplace le type de logement par le nom du foyer si "Foyer" est choisi
        if type_logement == "Foyer" and foyer:
            type_logement = foyer
        # Remplace le type de logement par le bailleur social si "Logement social est choisi
        if type_logement == "Logement social" and bailleur_social:
            type_logement = bailleur_social
        # Remplace le type de logement par le commentaire libre si "autre" est choisi
        if type_logement == "Autre" and autre_logement:
            type_logement = autre_logement
            
        # Enregistrement des données dans un fichier CSV
        data = [date, genre, age, provenance, qpv, type_logement, objet_demande, interne_amandiers, redirigee, commentaire]
        print("Export des données dans data.csv :\n",data)
        save_data(filename, data)

        # Retourne le même modèle HTML avec un message de succès
        return render_template('formulaire.html', today_date=today_date, message='Données enregistrées avec succès !')
    
    # Si la méthode est GET, simplement retourner le modèle HTML
    return render_template('formulaire.html',today_date=today_date)

@app.route('/group', methods=['GET', 'POST'])
def group():
    
    # Date actuelle au format ISO (AAAA-MM-JJ)
    today_date = dt.today().isoformat()  
    
    # Requête POST : Récupération des données du formulaire
    if request.method == 'POST':
        date_0 = request.form['date']
        objet_demande_0 = request.form['objet_demande']
        genre = request.form.getlist('genre[]')
        age = request.form.getlist('age[]')
        provenance = request.form.getlist('provenance[]')
        code_postal = request.form.getlist('code_postal[]') 
        qpv = request.form.getlist('qpv[]')
        type_logement = request.form.getlist('type_logement[]')
        autre_logement = request.form.getlist('precisez[]')
        commentaire = request.form.getlist('commentaire[]')
        
        # Indique les cases à cocher "traitement en interne" et "personne redirigée"
        objet_demande = [objet_demande_0] * len(qpv)
        date = [date_0] * len(qpv)
        interne_amandier = ["X"] * len(qpv)
        redirigee = [""] * len(qpv)
        
        # Réagence certains champs
        for ligne in range(0,len(interne_amandier)):
            provenance[ligne] = code_postal[ligne] if provenance[ligne] == "Autre code postal" and code_postal[ligne] else provenance[ligne]
            type_logement[ligne] = autre_logement[ligne] if type_logement[ligne] == "Autre" and autre_logement[ligne] else type_logement[ligne]
        
        print("Nombre de lignes à enregistrer :",len(qpv))
        print("Export des données dans data.csv :\n")
        
        # Enregistrement des données dans un fichier CSV
        for i in range (0,len(qpv)):
            data = [date[i], genre[i], age[i], provenance[i], qpv[i], type_logement[i], objet_demande[i], interne_amandier[i], redirigee[i], commentaire[i]]
            save_data(filename, data)
            print("ligne",i+1," ",data)
        print("Export des données terminé")

        # Retourne le même modèle HTML avec un message de succès
        return render_template('formulaire_groupe.html', today_date=today_date, message='Données enregistrées avec succès !')
    
    # Si la méthode est GET, simplement retourner le modèle HTML
    return render_template('formulaire_groupe.html',today_date=today_date)

@app.route('/massive', methods=['GET', 'POST'])
def massive():
    
    # Date actuelle au format ISO (AAAA-MM-JJ)
    today_date = dt.today().isoformat()  
    
    # Requête POST : Récupération des données du formulaire
    if request.method == 'POST':
        date = request.form.getlist('date[]')
        genre = request.form.getlist('genre[]')
        age = request.form.getlist('age[]')
        provenance = request.form.getlist('provenance[]')
        code_postal = request.form.getlist('code_postal[]') 
        qpv = request.form.getlist('qpv[]')
        type_logement = request.form.getlist('type_logement[]')
        autre_logement = request.form.getlist('precisez[]')
        objet_demande = request.form.getlist('objet_demande[]')
        interne_amandiers = request.form.getlist('interne_amandiers[]') 
        redirigee = request.form.getlist('interne_amandiers[]') 
        commentaire = request.form.getlist('commentaire[]')
        
        # Réagence certains champs
        for ligne in range(0,len(interne_amandiers)):
            interne_amandiers[ligne] = "X" if interne_amandiers[ligne] else ""
            redirigee[ligne] = "X" if redirigee[ligne] else ""
            provenance[ligne] = code_postal[ligne] if provenance[ligne] == "Autre code postal" and code_postal[ligne] else provenance[ligne]
            type_logement[ligne] = autre_logement[ligne] if type_logement[ligne] == "Autre" and autre_logement[ligne] else type_logement[ligne]

        print("Nombre de lignes à enregistrer :",len(qpv))
        print("Export des données dans data.csv :\n")
            
        # Enregistrement des données dans un fichier CSV
        for i in range (0,len(qpv)):
            data = [date[i], genre[i], age[i], provenance[i], qpv[i], type_logement[i], objet_demande[i], interne_amandiers[i], redirigee[i], commentaire[i]]
            save_data(filename, data)
            print("ligne",i+1," ",data)
        print("Export des données terminé")

        # Retourne le même modèle HTML avec un message de succès
        return render_template('formulaire_massif.html', today_date=today_date, message='Données enregistrées avec succès !')
    
    # Si la méthode est GET, simplement retourner le modèle HTML
    return render_template('formulaire_massif.html',today_date=today_date)


##### Recherche d'adresse pour autocomplétion
# Utilisation de l'API Adresse du gouvernement français
@app.route('/suggest_address')
def suggest_address():    
        query = request.args.get('q')
        # Instance locale OU celle de data.gouv.fr
        #api_url = 'http://localhost:7878/search/'
        api_url = 'https://api-adresse.data.gouv.fr/search/'
        response = requests.get(api_url, params={'q': query, 'limit': 10})
        if response.status_code == 200:
                data = response.json()
                suggestions = [{'properties': address['properties']} for address in data['features']]
                return jsonify(suggestions)
        else:
                return jsonify([])     


##### Récupèration des coordonnées correspondantes à une adresse donnée
@app.route('/get_coordinates')
def get_coordinates():
    address = request.args.get('address')
    # Instance locale OU celle de data.gouv.fr
    #api_url = 'http://localhost:7878/search/'
    api_url = 'https://api-adresse.data.gouv.fr/search/'
    response = requests.get(api_url, params={'q': address, 'limit': 1})
    if response.status_code == 200:
        data = response.json()
        if len(data['features']) > 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            return jsonify({'latitude': coordinates[1], 'longitude': coordinates[0]})
        else:
            return jsonify({'error': 'Adresse non trouvée'})
    else:
        return jsonify({'error': 'Erreur lors de la recherche des coordonnées'})


##### Vérifie pour un jeux de coordonnées données s'il est en zone QPV
# les zones géographiques QPV sont définis dans un fichier gpkg récupérable sur data.gouv
# https://www.data.gouv.fr/fr/datasets/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/
@app.route('/process_coordinates', methods=['POST'])
def process_coordinates():

    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    print("Vérification QPV pour la coordonnée :",latitude," ; ",longitude)
    
    # Obtention de la liste des couches disponibles du gpkg
    # La séparation de calques et leur concaténation dans un fichier gpkg peut être faite via Qgis
    layers = listlayers(fichier_gpkg)
    
    # Création d'un point à partir des coordonnées GPS
    point = Point(float(longitude), float(latitude))

    # Vérification si le point est à l'intérieur d'une des zones définies dans les couches
    for layer_name in layers:
        layer = read_file(fichier_gpkg, layer=layer_name)
        for idx, geom in enumerate(layer.geometry):
            if point.within(geom):
                print("Coordonnées trouvées dans la couche :", layer_name)
                # Retour formulaire avec l'information de la couche contenant le point
                return jsonify({'qpv_status': layer_name})

    print("Coordonnées hors QPV")
    # Retour formulaire avec l'information que le point est hors QPV
    return jsonify({'qpv_status': False})


# Fonction pour enregistrer des données dans un fichier CSV
def save_data(path, data):

    with open(path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        
        # Écrire les en-têtes de colonnes si le fichier est vide
        if file.tell() == 0:
            ### Partie à mettre à jour en cas de modifications des champs du formulaire
            writer.writerow(["Date", "Genre", "Âge", "Provenance", "Quartier prioritaire de la Ville", "Type de logement", "Objet de la demande", "Traitement en interne", "Personne redirigée", "Commentaire"])
            ### Fin de partie à mettre à jour
            
        # Écrire les données
        writer.writerow(data)

##### Lancer l'application Flask avec ou sans mode deboggage
# Indiquer les options ici
if __name__ == '__main__':
    #app.run(debug=True) # Mode hors ligne en mode débogage
    app.run(host="0.0.0.0") # Accessible depuis le réseau local 
