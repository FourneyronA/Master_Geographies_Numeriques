# -*- coding: utf-8 -*-
'''
Fichier créé le 29/11/2019
Master 2 Geonum
2C1 - Langages informatiques du Géoweb
'''

import http.client as client
import urllib.parse as parse
import json
from Xm import *

def centroide_points(points):
	"""
		Calcul du centroïde d'un ensemble de points
		paramètre "points" : contour du polygone
			une liste de points au format [ [lon1, lat1], [lon2, lat2], [lon3, lat3], ... ]
		sortie : un point au format [lon, lat]
	"""
	if len(points) > 0:
		x = 0.0
		y = 0.0
		for p in points:
			x += p[0]
			y += p[1]
		x /= len(points)
		y /= len(points)
		return {'lat': x, 'lon': y}
	else:
		return {'lat': 0, 'lon': 0}

def get_commerces(point):
    connection = client.HTTPSConnection("places.cit.api.here.com")
    connection.request("GET", "/places/v1/discover/search?"
                   + parse.urlencode({"in": str(point[1])+ "," + str(point[0]) + ";r=" + "500",
                                      "q":"commerces",
                                      "size": "2",
                                      "app_id":"{YOUR_APP_ID}",
                                      "app_code":"{YOUR_APP_CODE}"}),"",
                   {"Accept":"application/json"})
    commerces = []
    resp = connection.getresponse()
    if resp.status == client.OK:
        jsonData = json.JSONDecoder().decode(bytes.decode(resp.read()))
        for commerce in jsonData["results"]["items"]:
            commerces.append(commerce)
            #print("- " + commerce["title"] + " : (" + str(commerce["position"][1]) + ', ' + str(commerce["position"][0]) + ')')
    else:
        print("Erreur requête : " + str(resp.status))
    return commerces

print("Lignes de métro de Lyon et commerces proches d'une des extrémités des lignes")

connection = client.HTTPSConnection("download.data.grandlyon.com")

#https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=tcl_sytral.tcllignemf&outputFormat=application/json; subtype=geojson&SRSNAME=EPSG:4326&startIndex=0
connection.request("GET", "/wfs/rdata?" +
                   parse.urlencode({"SERVICE": "WFS",
                                    "VERSION": "2.0.0",
                                    "request": "GetFeature",
                                    "typename": "tcl_sytral.tcllignemf",
                                    "SRSNAME": "EPSG:4326",
                                    "outputFormat": "geojson",
                                    "startIndex": "0"}), "",
                   {"Accept": "application/json"})

resp = connection.getresponse()
print("HTTP Rest : download.data.grandlyon.com, résultat " + str(resp.status))

metros = []
tcl = {}
if resp.status == client.OK:
    print("---------------------------")
    tcl = json.JSONDecoder().decode(bytes.decode(resp.read()))
    for metro in tcl["features"]:
        if (metro["properties"]["sens"] == "Aller"): # On ne prend que les sens "Aller" pour éviter les doublons de ligne
            metros.append(metro)
            print("- " + metro["properties"]["ligne"] + ' ' + metro["properties"]["libelle"])
else :
    print(resp.status)

for metro in metros:
    commerces = get_commerces(metro["geometry"]["coordinates"][0])
    print("-------------------------")
    print("Commerces proches de la ligne " + metro["properties"]["ligne"] + ', ' + str(metro["geometry"]["coordinates"][0]) + " : ")
    for commerce in commerces:
        print("- " + commerce["title"] + " : (" + str(commerce["position"][1]) + ', ' + str(
            commerce["position"][0]) + ')')

# Préparation du document
xm = Xm()

# Première balise kml racine
main = xm.group('kml', {"xmlns": "http://www.opengis.net/kml/2.2"}, [])

# Balise Document
document = xm.group("Document", {}, [xm.text("name", {}, "Lignes de métro à Lyon et commerces proches d'une extrémité (500m)")])

# Balise Style styleCommerces
styleCommerces = xm.group("Style", {"id": "styleCommerces"}, [])
# Balise IconStyle
icon_style = xm.group("IconStyle", {}, [xm.text("color", {}, "ffff0000")])
# Balise Icon
#icon = xm.group("Icon", {}, [xm.text("href", {}, "http://maps.google.com/intl/en_us/mapfiles/ms/micons/yellow.png")])
#xm.text("href", {}, "http://maps.google.com/intl/en_us/mapfiles/ms/micons/yellow.png")
# On ajoute la balise Icon à la balise IconStyle
#xm.add(icon_style, icon)
xm.add(icon_style, xm.text("scale", {}, 1.4))
# On ajoute la balise IconStyle à la balise Style styleCommerces
xm.add(styleCommerces, icon_style)
# Balise LabelStyle
label_style = xm.group("LabelStyle", {}, [xm.text("color", {}, "b84451ff"), xm.text("scale", {}, 0.7)])
# On ajoute la balise LabelStyle à la balise Style styleCommerces
xm.add(styleCommerces, label_style)
# Balise LineStyle
line_style = xm.group("LineStyle", {}, [xm.text("color", {}, "ff00ffff"), xm.text("width", {}, 2)])
# On ajoute la balise LabelStyle à la balise Style styleCommerces
xm.add(styleCommerces, line_style)
# On ajoute la balise Style stylePOIs à la balise Document
xm.add(document, styleCommerces)

# Balise Style styleMetros
styleMetros = xm.group("Style", {"id": "styleMetros"}, [])
# Balise LineStyle
line_style = xm.group("LineStyle", {}, [xm.text("color", {}, "ff336699"), xm.text("width", {}, 5)])
# On ajoute la balise LabelStyle à la balise Style styleCommerces
xm.add(styleMetros, line_style)
# On ajoute la balise Style stylePOIs à la balise Document
xm.add(document, styleMetros)

# Balise Folder Lignes de métro
lignes_metro = xm.group("Folder", {}, [xm.text("name", {}, "Lignes de métro"), xm.text("open", {}, 0)])
for ligne in tcl["features"]:
    if (ligne["properties"]["sens"] == "Aller"): # On remet le filtre pour n'avoir qu'une seule fois la ligne de métro (sens Aller)
        # Balise Placemark
        placemark = xm.group('Placemark', {}, [xm.text('name', {}, ligne["properties"]["ligne"]), xm.text('styleUrl', {}, "#styleMetros")])
        # Balise ExtendedData
        extData = xm.group('ExtendedData', {}, [])
        # Balise Data
        data = xm.group('Data', {'name': "ligne"}, [xm.text('value', {}, ligne["properties"]["ligne"])])
        #On ajoute la balise Data à la balise ExtendedData
        xm.add(extData, data)
        # Balise Data
        data = xm.group('Data', {'name': "tracé"}, [xm.text('value', {}, ligne["properties"]["libelle"])])
        #On ajoute la balise Data à la balise ExtendedData
        xm.add(extData, data)
        # Balise Data
        origine_str = str(ligne["properties"]["libelle"]).split(' - ')[0]
        data = xm.group('Data', {'name': "origine"}, [xm.text('value', {}, origine_str)])
        #On ajoute la balise Data à la balise ExtendedData
        xm.add(extData, data)
        # Balise Data
        destination_str = str(ligne["properties"]["libelle"]).split(' - ')[1]
        data = xm.group('Data', {'name': "destination"}, [xm.text('value', {}, destination_str)])
        #On ajoute la balise Data à la balise ExtendedData
        xm.add(extData, data)
        # Balise Data
        type = 'FUN' if str(ligne["properties"]["ligne"]).startswith('F') else 'MET' # Opérateur ternaire
        data = xm.group('Data', {'name': "type"}, [xm.text('value', {}, type)])
        #On ajoute la balise Data à la balise ExtendedData
        xm.add(extData, data)
        # On ajoute la balise ExtendedData à la balise Placemark
        xm.add(placemark, extData)
        # Balise MultiGeometry
        multigeom = xm.group('MultiGeometry', {}, [])
        # Balise Point
        # --------------------------------------
        # Avec le premier point de la ligne
        # point = xm.group('Point', {}, [xm.text('coordinates', {}, str(ligne["geometry"]["coordinates"][0][0]) + ',' +
        #                                        str(ligne["geometry"]["coordinates"][0][1]) + ',' +
        #                                        '0.0')])
        # --------------------------------------
        # --------------------------------------
        # Avec le centroïde de la ligne
        centre_ligne = centroide_points(ligne['geometry']["coordinates"])
        point = xm.group('Point', {}, [xm.text('coordinates', {}, str(centre_ligne['lat']) + ',' +
                                               str(centre_ligne['lon']) + ',' +
                                               '0.0')])
        # --------------------------------------
        # On ajoute la balise Point à la balise MultiGeometry
        xm.add(multigeom, point)
        coordinates = []
        for coord in ligne["geometry"]["coordinates"]:
            point = []
            for i in coord:
                point.append(str(i))
            coordinates.append(','.join(point))
            str_line = ' '.join(coordinates)
        # Balise LineString
        line = xm.group('LineString', {}, [xm.text("tessellate", {}, 1),
                                           xm.text("coordinates", {}, str_line)])
        # On ajoute la balise LineString à la balise Placemark
        xm.add(multigeom, line)
        # On ajoute la balise MultiGeometry à la balise Placemark
        xm.add(placemark, multigeom)
        # On ajoute la balise Placemark à la balise Folder Lignes de métro
        xm.add(lignes_metro, placemark)
# On ajoute la balise Folder Lignes de métro à la balise Document
xm.add(document, lignes_metro)

# Balise Folder Commerces
folder_commerces = xm.group("Folder", {}, [xm.text("name", {}, "Commerces"), xm.text("open", {}, 0)])
for ligne in tcl["features"]:
    if (ligne["properties"]["sens"] == "Aller"): # On remet le filtre pour n'avoir qu'une seule fois la ligne de métro (sens Aller)
        commerces = get_commerces(ligne["geometry"]["coordinates"][0])
        for commerce in commerces:
            # Balise Placemark
            placemark = xm.group('Placemark', {}, [xm.text('name', {}, commerce["title"]), xm.text('styleUrl', {}, "#styleCommerces")])
            # Balise ExtendedData
            extData = xm.group('ExtendedData', {}, [])
            # Balise Data
            data = xm.group('Data', {'name': "nom"}, [xm.text('value', {}, commerce["title"])])
            # On ajoute la balise Data à la balise ExtendedData
            xm.add(extData, data)
            # Balise Data
            data = xm.group('Data', {'name': "notation"}, [xm.text('value', {}, commerce["averageRating"])])
            # On ajoute la balise Data à la balise ExtendedData
            xm.add(extData, data)
            # Balise Data
            data = xm.group('Data', {'name': "adresse"}, [xm.text('value', {}, commerce["vicinity"])])
            # On ajoute la balise Data à la balise ExtendedData
            xm.add(extData, data)
            # On ajoute la balise ExtendedData à la balise Placemark
            xm.add(placemark, extData)
            # Balise MultiGeometry
            multigeom = xm.group('MultiGeometry', {}, [])
            # Balise Point
            point = xm.group('Point', {}, [xm.text('coordinates', {}, str(commerce["position"][1]) + ',' +
                                                   str(commerce["position"][0]) + ',' +
                                                   '0.0')])
            # On ajoute la balise Point à la balise MultiGeometry
            xm.add(multigeom, point)
            # Balise LineString
            line = xm.group('LineString', {}, [xm.text('coordinates', {}, str(commerce["position"][1]) + ',' +
                                                   str(commerce["position"][0]) + ',' +
                                                   '0.0' + ' ' +
                                                    str(ligne["geometry"]["coordinates"][0][0]) + ',' +
                                                    str(ligne["geometry"]["coordinates"][0][1]) + ',' + '0.0'
                                                       )])
            # On ajoute la balise Point à la balise MultiGeometry
            xm.add(multigeom, line)
            # On ajoute la balise MultiGeometry à la balise Placemark
            xm.add(placemark, multigeom)
            # On ajoute la balise Placemark à la balise Folder Commerces
            xm.add(folder_commerces, placemark)
# On ajoute la balise Folder Lieux visités à la balise Document
xm.add(document, folder_commerces)

# On ajoute la balise Document à la balise kml racine
xm.add(main, document)
# Déclaration de la balise racine
xm.root(main)

print(xm.tostring())
# Export de l'arborescence vers un fichier KML
xm.tofile("metros_commerces.kml")