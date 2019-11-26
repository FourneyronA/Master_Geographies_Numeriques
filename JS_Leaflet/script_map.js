var map = L.map('map');

var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var osmAttrib = 'Map data © OpenStreetMap Contributeur';

var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);

// définir les paramètre de visualisation de la carte
map.setView([45.72,4.88],12);


// ajouter un maker
var marker = L.marker([45.7238, 4.8324]);
marker.addTo(map);
// map.setView([Lattitude,Longitude],Niveau de Zoom); (Niveau de zoom = )



// icone personnaliser 
var schoolIcon = L.icon({
    iconUrl: 'leaflet/images/marker-icon.png'
 
});

// 
var circle_marker = L.circleMarker([45.7238, 4.8324], {
    radius:25,
    color : '#7c1e70',
    weight : 0.5
    });
circle_marker.addTo(map);



// EXO 

var ligne_tram = [[4.91556, 45.7221],[4.91735, 45.71945],[4.92218, 45.72033],[4.92518, 45.7184]];
var tram = [[45.71963, 4.91796],[45.7184, 4.92518],[45.7221, 4.91556]];
var parking = ["4.91789, 45.71875", "4.91832, 45.71894", "4.91874, 45.71792", "4.91843, 45.71766"];


// ajouter les stations de tram du tableau
for (var i=0; i < tram.length; i++){
    // mise du maker pour chaque station
    L.marker(tram[i]); //.addTo(map);
    // mise d'un cercle de 500px pour chaque station
    L.circle(tram[i], 500, {color : 'pink', fillOpacity:0.5}); //.addTo(map);
}


// ajouter une la ligne du tram à partir des différents points de ligne du tram
// création d'un objet polyligne
var tram_trace = L.polyline([], {
    "color": "black", 
    "weight": 2
})

// ajout de coordonnée dans l'objet polyligne à partir des points du tableau
for(var i=0; i < ligne_tram.length; i++){
    // reverse permet d'inverser les coordonnée
    tram_trace.addLatLng(ligne_tram[i].reverse());
}


// ajouter un poligon du parking à partir des points de coordonée du parkings 
// création du tableau 
coord_parking = [];
for (var i=0; i < parking.length; i++){
    coord_parking.push(parking[i].split(', ').reverse());
}

var parkingP = L.polygon(coord_parking, {
    "fillColor":"red",
    "fillOpacity": 1,
    "weight": 0
})





// Generer un maker aleatoire 
/*
var Nom_maker = prompt("Nom du maker à ajouter ?")
// recupération de la fenetre 
var bounds = map.getBounds();
// placer des point aléatoire en fonction de la taille de la fenetre
var x = bounds.getEast() + Math.random()*(bounds.getWest() - bounds.getEast());
var y = bounds.getSouth() + Math.random()*(bounds.getNorth() - bounds.getSouth());

var marker =L.marker([y,x]).addTo(map).bindTooltip(Nom_maker+ " " + x + " " + y, {permanent : false});
*/


// ajouter des données à partir d'un fichier geoJSON
// le géoJSON à plusieurs paramètres, tables associé
// il repère automatiquement la géométrie
// cependant utiliser les variables liées il faut : 
// Variable_geoJSON.properties.NOMDELAVARIABLE 

// EXO N°0
// Affichier un geoJSON de point avec un style et une pop de texte adapté 
var Velov = L.geoJSON(data, {
    pointToLayer: function(feature, latlng){
        var NOM = feature.properties.Name.split("-")[1]; // autres solutions feature.properties.Name.substring(0,3)
        var CODE = feature.properties.Name.split("-")[0]; // feature.properties.Name.substring(5,feature.properties.Name.length)
        var schoolIcon = L.icon({
            iconUrl: 'leaflet/images/marker-icon.png'
        });

    return L.marker(latlng, {icon : schoolIcon}).bindTooltip(
        "Code :"+ CODE + 
        "<br>Nom :"+NOM +
        "<br> type : "+feature.geometry.type,
        {permanent : false}); 
    }
})




// EXO N°1 
// Attention pour la taille du GeoJSON toujours penser à aleger les fichiers pour celà on peu :
// N°1 -> prendre seulement les données utiles
// N°2 -> changer la précision de QGIS (15 décimale suivant la précision souhaiter on peut revenir à 7)
// N°3 -> Simplifier la forme géométrique (mappshapper)
function gettaux_20(feature){
    var taux_vingt = (feature.properties._pop20 / ( feature.properties._pop65+ feature.properties._pop20 + feature.properties._pop20))*100;
    return taux_vingt;
}

function getColortaux(feature){
    var d = (feature.properties._pop20 / ( feature.properties._pop65+ feature.properties._pop20 + feature.properties._pop20))*100;
    return d > 40 ? '#800026' :
    d > 38  ? '#BD0026' :
    d > 36  ? '#E31A1C' :
    d > 34  ? '#FC4E2A' :
    d > 32   ? '#FD8D3C' :
    d > 30   ? '#FEB24C' :
    d > 25   ? '#FED976' :
               '#FFEDA0';
    };

    function getColor(d) {
        return d > 1000 ? '#800026' :
               d > 500  ? '#BD0026' :
               d > 200  ? '#E31A1C' :
               d > 100  ? '#FC4E2A' :
               d > 50   ? '#FD8D3C' :
               d > 20   ? '#FEB24C' :
               d > 10   ? '#FED976' :
                          '#FFEDA0';
    };

    function Fstyle(feature) {
        return {fillColor: getColortaux(feature),
            weight: 1,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.7};
    };

    function zoom(feature, layer) {
        layer.on('click', function(){
            map.fitBounds(layer.getBounds())
        })
        layer.bindPopup("Nom :"+ feature.properties.nom + 
        "<br>Taux :"+ gettaux_20(feature) +
        "<br>Nombre : "+feature.properties._pop20,
        {permanent : false});
    };

    var commune = L.geoJson(data_exo1, {
        style: Fstyle,
        onEachFeature: zoom
    }).addTo(map);

   

var commune = L.geoJson(data_exo1, {
        style: style(feature) ,
        onEachFeature: function (feature, layer) {
            layer.bindPopup("Nom :"+ feature.properties.nom + 
            "<br>Taux :"+ gettaux_20(feature) +
            "<br>Nombre : "+feature.properties._pop20,
            {permanent : false});
        }
    }).addTo(map);


// zoom automatique de la fenetre sur les variables :
map.fitBounds(commune.getBounds())






// gestion des fond de plan
var baseLayers = {
    "OpenStreetMap":osm
};

// gestion des couches qui ce superpose aux fond de plan 
var overlays = {
    "Velov": Velov,
    "Commune": commune,
    "Autres " : tram_trace, parkingP
};

L.control.layers(baseLayers, overlays).addTo(map);





/*
for (var i=0; i < ligne_tram.length; i++){
    L.polyline(ligne_tram[i].reverse()).addTo(map);
}
/*

parking.replace("\"","[")
for (var i=0; i < parking.length; i++){
    L.marker(parking[i].reverse(),  {icon: schoolIcon}).addTo(map);
}
// ajouter une ligne 
var line = L.polyline(ligne_tram, {color : 'blue', fillOpacity:0.5});
line.addTo(map);









// EXEMPLE POSSIBILITEE

/*
// ajouter un maker
var marker = L.marker([45.7238, 4.8324]);
marker.addTo(map);
// map.setView([Lattitude,Longitude],Niveau de Zoom); (Niveau de zoom = )


// ajouter un cercle avec un cercle en mètre 
var cercle = L.circle([45.730,4.85], 500, {color : 'pink', fillOpacity:0.5});
cercle.addTo(map);

// ajouter une ligne 
var line = L.polyline([[45.722,4.8322],[45.725,4.8322],[45.725,4.8326]], {color : 'blue', fillOpacity:0.5});
line.bindTooltip("<b> Mes options </b> <br> et bien plus encore", {
    className : 'line_test',
   
    permanent : false});
line.addTo(map);

// ajouter un polygone
var polygone = L.polygon(
    [[45.722,4.8321],[45.725,4.8322],[45.725,4.8325],[45.722,4.85]],
     {color : 'red', fillOpacity:0.8});
polygone.addTo(map);


// ajouter un rectangle
var polygone = L.rectangle(
    [[45.722,4.8321],[45.725,4.8322],[45.725,4.8325]],
     {color : 'green', fillOpacity:0.5});
polygone.addTo(map);

// ajouter un cercle avec une longeur en pixel 
var circle_marker = L.circleMarker([45.7238, 4.8324], {
    radius:25,
    color : '#7c1e70',
    weight : 0.5
    });
circle_marker.addTo(map);




var maker2 = L.marker([45.730,4.85], {icon: schoolIcon});
maker2.addTo(map);
*/