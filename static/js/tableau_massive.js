// Ajout d'une nouvelle ligne au tableau, avec tous les champs
function addRow(todayDate) {
    var table = document.getElementById("grouped-fields").getElementsByTagName('tbody')[0];
    // Décompte du nombre de ligne
    var rowCount = table.rows.length;
    // Ajout de la nouvelle ligne
    var newRow = table.insertRow();
    newRow.innerHTML = '<td><input type="date" name="date[]" value="' + todayDate + '" required></td>' +
	'<td><input type="number" name="age[]" placeholder="Âge" required style="margin-right: 5px; width: 6ch" ></td>' +
	'<td>' +
	    '<select name="genre[]" style="width: 4ch" required>' +
	        '<option value="" disabled selected hidden></option>' +
	        '<option value="M">M</option>' +
	        '<option value="F">F</option>' +
	        '<option value="Autre">-</option>' +
	    '</select>' +
	'</td>' +
	'<td>' +
	    '<select name="provenance[]" required>' +
	        '<option value="" disabled selected hidden></option>' +
	        '<option value="Quartier des Amandiers">Amandiers</option>' +
	        '<option value="Autre 20ème">Autre 20ème</option>' +
	        '<option value="Autre code postal">Autre CP</option>' +
	    '</select>' +
	'</td>' +
	'<td><input type="text" name="code_postal[]" style="width: 5ch"></td>' +
	'<td>' +
	    '<select name="qpv[]" required>' +
	        '<option value="" disabled selected hidden></option>' +
	        '<option value="Non renseigné">?</option>' +
	        '<option value="Amandiers">Amandiers</option>' +
	        '<option value="Porte 20ème">Porte 20ème</option>' +
	        '<option value="Autre QPV">Autre QPV</option>' +
	        '<option value="Hors QPV">Hors QPV</option>' +
	    '</select>' +
	'</td>' +
	'<td>' +
	    '<select name="type_logement[]" required>' +
	        '<option value="" disabled selected hidden></option>' +
	        '<option value="Paris Habitat">Paris Habitat</option>' +
	        '<option value="RIVP">RIVP</option>' +
	        '<option value="Elogie">Elogie</option>' +
	        '<option value="Autre bailleur social">Autre social</option>' +
	        '<option value="Coalia">Foyer Coalia</option>' +
	        '<option value="ADEF">Foyer ADEF</option>' +
	        '<option value="Adoma">Foyer Adoma</option>' +
	        '<option value="Logement privé">Logement privé</option>' +
	        '<option value="Autre">Autre (préciser)</option>' +
	    '</select>' +
	'</td>' +
	'<td><input type="text" style="width:13ch" name="precisez[]" maxlength="50"></td>' +
	'<td><input type="checkbox" name="interne_amandiers[]" value="1"></td>' +
	'<td><input type="checkbox" name="redirigee[]" value="1"></td>' +
	'<td><input name="objet_demande[]" style="width:13ch" required></td>' +
	'<td><input type="text" style="width:13ch" name="commentaire[]"></td>' +
	'<td><button type="button" onclick="deleteRow(this)"><span><img src=/static/eraser-solid.svg></span></button></td>';
}

// Supression de la dernière ligne

function deleteRow(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
}
