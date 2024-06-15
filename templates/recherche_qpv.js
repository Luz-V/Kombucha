// Fonction de suggestion d'adresse basée sur le script précédent
// Nombre de valeurs paramétrable dans /suggest_address (voir formulaire_mix.py)

$(document).ready(function(){
    $('#adresse').on('input', function(){
        var input = $(this).val();
        // Activation de l'autocomplétion à partir de 3 caractères
        if (input.length >= 3) {
            // Requête GET à la route /suggest_address
            $.get('/suggest_address', {'q': input}, function(data){
                // Vidange des suggestion pour éviter la pollution
                $('#suggestions').empty();
                // Ajout des valeurs à la liste 'Suggestion'
                data.forEach(function(suggestion){
                    $('#suggestions').append('<option value="' + suggestion.properties.label + '">');
                });
            });
        }
    });
                
    // Vérification de la présence de l'adresse dans la base de donnée QPV   
    function verifierQPV() {
        var selectedAddress = $('#adresse').val();
        if (selectedAddress) {
            // Requête POST à la route /get_coordinate avec l'adresse postale 
            // Récupération des coordonnées (si l'adresse est trouvée dans la base)
            $.get('/get_coordinates', {'address': selectedAddress}, function(data){
                if ('latitude' in data && 'longitude' in data) {
                    // Requête POST à la route /process_coordinates avec les coordonées
                    $.post('/process_coordinates', {'latitude': data.latitude, 'longitude': data.longitude}, function(response){
                        // Mise à jour du champ QPV en fonction du calque dans lequel est trouvé le point de coordonné (voir 'mettreAJourQPV')
                        mettreAJourQPV(response.qpv_status);
                    });
                // Si l'adresse n'est pas trouvée dans la base
                } else {
                    alert('Adresse non trouvée');
                }
            });
        } else {
            alert("Veuillez entrer une adresse avant de vérifier le QPV.");
        }
    }

    // Associer la fonction verifierQPV à l'événement clic du bouton "verifierQPV"
    $('#verifierQPV').on('click', verifierQPV);
});

// Mise à jour de la valeur du champ QPV en fonction du résultat de la recherche QPV
// Dans le cas présent, on distingue les zones QPV Amandiers, QPV Porte 20ème, QPV autres, et les zones Hors QPV
// Cette distinction implique des calques séparés pour les 3 zones QPV dans le fichier gpkg
// La séparation de ces calques a été faite en amont via Qgis.

function mettreAJourQPV(NomQPV) {
    var qpvSelect = document.getElementById("qpv");
    // Section à modifier en cas d'utilisation d'un fichier gpkg générique
    if (NomQPV) {
        if (NomQPV === "QPV_amandiers") {
            alert("Adresse en QPV Amandiers")
            qpvSelect.value = "Amandiers";
        } else if (NomQPV === "QPV_P20_WGS84") {
            alert("Adresse en QPV Porte 20eme")
            qpvSelect.value = "Porte 20ème";
        } else if (NomQPV === "QPV_autres_WGS84") {
            alert("Adresse en QPV (autres)")
            qpvSelect.value = "Autre QPV";
        } 
    }
    else {
        alert("Adresse Hors QPV")
        qpvSelect.value = "Hors QPV";
    }
}
