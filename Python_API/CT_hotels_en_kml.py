#Ce script permet d'aller requeter les hotels dans les quartiers de lyon (buffer fixe à partir du centroide), 
#et de créer un kml qui contient la géométrie des quartiers et des hotels



import http.client as client
import urllib.parse as parse
import json
from math import *
from Xm import *



#La fonction pour obtenir le centroide de nos quartier
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
	a /= 2;
	x /= 6 * a;
	y /= 6 * a;
	#Pour des raisons un peu à la con, on sort le résultat dans un tableau qui contient un premier élément en tableau et un deuxième en string
	# On aura : [[x, y], ["x,y"]]
	return [x, y], str(y) + ',' + str(x)


#Récupération des quartiers : 
connectionGL = client.HTTPSConnection("download.data.grandlyon.com")
connectionGL.request("GET", "/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=adr_voie_lieu.adrquartier&SRSNAME=EPSG:4326&outputFormat=application/json;%20subtype=geojson&count=5&startIndex=15")
respGL = connectionGL.getresponse()
#On imprime le statut de la requete
print(respGL.status)

#On prépare le ficher kml
xm = Xm()
#Première balise kml
main = xm.group('kml', {}, [])
#Deuxième balise Document
doc = xm.group('Document', {}, [xm.text("name", {}, 'Hotels à Lyon')])
#On ajoute la balise Document dans notre balise kml
xm.add(main, doc )
#Si le statut de la requete est ok (c'est-à-dire si il affiche 200), on continue :
if respGL.status == client.OK:
	#On imprime des trucs pour que ce soit joli :
	print("------------------------------------")
	print("Quartiers de Lyon:")
	#On stocke dans la variable jsonDATAGL la réponse à notre requete
	jsonDataGL = json.JSONDecoder().decode(bytes.decode(respGL.read()))
	#On va ensuite itérer sur les features de cette réponse
	#	Chaque itération sera stockée dans la variable "quartier" --> quartier est donc une variable qui contient un élément d'un dictionnaire qui a la même structure d'un geojson, avec ses properties et sa geometry
	for quartier in jsonDataGL["features"]:
		#On commence par stocker la géométrie de cet élément dans une variable geom (geom est donc une liste de couples de coordonnées [x, y])
		geom = quartier["geometry"]["coordinates"][0]
		#On peut donc appeler la fonction centroide pour récupérer le centroide de notre quartier, en donnant en argument cette liste de coordonnées
		centro = centroide(geom)
		#On affiche des trucs pour que ce soit joli
		print("----------------------------------------------------------------")
		print(quartier["properties"]["nom"] + " : "+ str(centro[0]))

		#Toute cette partie concerne la construction du kml
		#Chaque polygone est contenue dans une balise Placemark
		place = xm.group('Placemark', {}, [])
		#Cette balise Placemark a un nom : on va cherche le nom de notre élément dans le dictionnaire (quartier["properties"]["nom"]) :
		name = xm.text('name', {}, quartier["properties"]["nom"])
		#On ajoute cette balise dans la balise Document
		xm.add(doc, place)
		#On crée ensuite la balise Polygone, qui a quelques éléments textes à l'intérieur
		geometrie = xm.group('Polygon', {}, [
			xm.text('extrude', {}, 0), #Premier élément texte
			xm.text('tessellate', {}, 0), #Deuxième élément texte
			xm.text('altitudeMode', {}, "clampToGround"), #Troisième élément texte
			]) #Fin de la balise Polygone
		#On ajoute notre balise Polygone dans Placemark
		xm.add(place, geometrie)
		#On crée une balise OuterBoundaryIs
		bound = xm.group('outerBoundaryIs', {}, [])
		#On l'ajoute dans Polygon
		xm.add(geometrie, bound)
		#On crée une balise LinearRing
		ring = xm.group('LinearRing', {}, [])
		#On l'ajoute dans OuterBoundaryIs
		xm.add(bound, ring)
		#On s'occupe ensuite des coordonnées, qui doivent être fournies dans la balise "coordinates" selon le format suivante : "x,y x,y x,y"
		#On va stocker cette chaine de caractère dans une variable coords
		coords = ""
		#On se balade dans la variable geom qui contient la liste des couples de coordonnées
		for couple in geom:
			#On récupère en chaine de caractère chaque coordonnée et on les sépare par une virgule.
			#On concatène à chaque tour d'itération dans la variable coords
			#On ajoute un espace à la fin pour bien séparer nos chaines de caractère
			coords = coords + str(couple[0]) +','+ str(couple[1]) + ' '
		#On ajoute le tout dans la balise "coordinates"
		coordonnee = xm.text('coordinates', {}, coords)
		#On ajoute cette balise dans la balise LineaRing
		xm.add(ring, coordonnee)

	#Récupération de la liste des hotels : 
		#On ouvre une nouvelle connexion, à Here pour récupérer les hotels dans notre quartier
		connection = client.HTTPSConnection("places.cit.api.here.com")
		connection.request("GET", "/places/v1/autosuggest?"+parse.urlencode({"in":centro[1] + ";r=500", "q":"hotels", "app_id":"uDVwlDAVmF377kRVXkFT", "app_code": "E1RXzAWIIq5IqjMl09YxHQ"}))
		resp = connection.getresponse()
		print(resp.status)
		#On vérifie si la connection est bonne
		if resp.status == client.OK:
			#On stocke le résultat dans la variable jsonDATA, qui contient donc un dictionnaire, mais qui n'a pas la structure geojson cette fois-ci
			#	 -> c'est une structure propre à Here
			jsonData = json.JSONDecoder().decode(bytes.decode(resp.read()))
			#On se balade dans nos "features". À chaque tour, la variable "hotel" contient une feature de notre geojson
			for hotel in jsonData["results"]:
				#On vérifie qu'on n'est pas dans les objets génériques qui s'appelle "hotels" ou "Hostels" -> ces entités n'ont pas de géométrie 
				#		(encore une spécificité de Here, ça change pas grand chose mais ça fait planter le truc sinon)
				if hotel["title"] != "hotels" and hotel["title"] !='Hostels' :
					#On affiche des trucs pour que ce soit joli
					print("-"+hotel["title"])

					#Cette partie concerne la construction du fichier KML
					#À nouveau, chaque entité est stockée dans une variable Placemark
					place = xm.group('Placemark', {}, [])
					#On crée la balise name, et on va cherche le nom de l'hotel, qui est cette fois-ci dans hotel["title"]
					name = xm.text('name', {}, hotel["title"])
					#On crée la balise Point qui va contenir les coordonnées
					point = xm.group('Point',{}, [])
					#On crée la balise coordonnée, en transformant en string et en concaténant (séparés par une virgule), nos x et y qui sont stocké dans une liste de type : position[x, y]
					coords = xm.text('coordinates', {}, str(hotel["position"][1]) + ',' + str(hotel["position"][0]))
					#On emboite le tout : place dans doc, name dans place, point dans place, coords dans point
					xm.add(doc, place)
					xm.add(place, name)
					xm.add(place, point)
					xm.add(point, coords)

#On définit la racine
xm.root(main)
#On crée le fichier
xm.tofile('hotellyon.kml')
#Voilàààà !!
#On peut ouvrir dans GoogleEarth le kml