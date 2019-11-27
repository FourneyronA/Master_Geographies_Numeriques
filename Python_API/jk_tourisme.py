#!/usr/bin/env python3

import requests
import json
from yattag import Doc, indent

APP_ID = "1uzNinZ9iqcQcp9REnsf"
APP_CODE = "tHNUpzmaJKcxiJdNJ2VM6Q"

#
# Fonctions outils
#

def centroide(points):
	"""
	paramètre "points" : une liste de points de la forme :
		[[40.1, 4.2], [41.3, 3.5], ...]
	"""
	a = 0
	x = 0
	y = 0
	for i in range(len(points) - 1):
		d = points[i][0] * points[i+1][1] - points[i+1][0] * points[i][1]
		a += d
		x += ( points[i][0] + points[i+1][0] ) * d
		y += ( points[i][1] + points[i+1][1] ) * d
	a /= 2
	x /= 6 * a
	y /= 6 * a
	return {'lat': x, 'lon': y}

def kmlOutput(features, path):
	doc, tag, text, line = Doc().ttl()
	doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
	with tag('kml', xmlns="http://www.opengis.net/kml/2.2"):
		with tag('Document'):	
			for feature in features:
				with tag('Placemark'):
					line('Name', feature["title"])
					line('Description', '')
					with tag('Point'):
						line('coordinates', "%s,%s,0"%(feature["position"][1], feature["position"][0]))
	file = open(path, "w")
	file.write(indent(doc.getvalue()))
	file.close()

#
# Programme principal
#

# Récupération des quartiers
quartiers = []
url = "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=adr_voie_lieu.adrquartier&outputFormat=application/json;%20subtype=geojson&SRSNAME=EPSG:4326&startIndex=0&count=20"
resp = requests.get(url)
if resp.status_code == requests.codes.ok :
    jsonData = json.JSONDecoder().decode(resp.text)
    for quartier in jsonData["features"]:
        quartiers.append(quartier)

# Récupération des restaurants
hotels = []
for quartier in quartiers:
    polygon = quartier["geometry"]["coordinates"]
    centre = centroide(polygon[0])
    url = "https://places.cit.api.here.com/places/v1/discover/search?in=%s,%s;r=%s&q=%s&app_id=%s&app_code=%s"\
        %(centre["lon"], centre["lat"], 500, "hotel", APP_ID, APP_CODE)
    resp = requests.get(url)
    if resp.status_code == requests.codes.ok :
        jsonData = json.JSONDecoder().decode(resp.text)
        for hotel in jsonData["results"]["items"]:
            hotels.append(hotel)

kmlOutput(hotels, "output.kml")