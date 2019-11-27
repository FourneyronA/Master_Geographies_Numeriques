import http.client as client
import urllib.parse as parse
import json

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
	return {'lat': x, 'lon': y}

connection = client.HTTPSConnection("download.data.grandlyon.com")

#https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=adr_voie_lieu.adrquartier&SRSNAME=EPSG%3A4326&outputFormat=application%2Fjson%3B+subtype%3A+geojson&count=5&startIndex=1
#https://download.data.grandlyon.com/ws/grandlyon/adr_voie_lieu.adrquartier/all.json?maxfeatures=100&start=1
# connection.request("GET", "/ws/grandlyon/adr_voie_lieu.adrquartier/all.json?" +
#                    parse.urlencode({"maxfeatures": "5", "start": "1"}), "",
#                    {"Accept": "application/json"})
connection.request("GET", "/wfs/grandlyon?" +
                   parse.urlencode({"SERVICE": "WFS", "VERSION": "2.0.0", "request": "GetFeature", "typename": "adr_voie_lieu.adrquartier",
                                    "SRSNAME": "EPSG:4326", "outputFormat": "geojson", "count": "5", "startIndex": "1"}), "",
                   {"Accept": "application/json"})

resp = connection.getresponse()
quartiers = []
if resp.status == client.OK:
    print("---------------------------")
    print("Liste des quartiers de Lyon")
    jsonData = json.JSONDecoder().decode(bytes.decode(resp.read()))
    for quartier in jsonData["features"]:
        quartiers.append(quartier)
        print("- " + quartier["properties"]["nom"])
else :
    print(resp.status)

for quartier in quartiers:
    polygon = quartier["geometry"]["coordinates"]
    centre = centroide(polygon[0])
    connection = client.HTTPSConnection("maps.googleapis.com")
    # requete = "/maps/api/place/nearbysearch/json?" + parse.urlencode({"location": str(centre["lon"]) + "," + str(centre["lat"]),
    #                                                                   "radius": "1500",
    #                                                                   "type": "lodging",
    #                                                                   "key": "YOUR_KEY"})
    # print(requete)
    connection.request("GET", "/maps/api/place/nearbysearch/json?" +
                       parse.urlencode({"location": str(centre["lon"]) + "," + str(centre["lat"]),
                                        "radius": "500",
                                        "type": "lodging",
                                        "key": "YOUR_KEY"}), "",
                       {"Accept": "application/json"})
    resp = connection.getresponse()
    if resp.status == client.OK:
        jsonData = json.JSONDecoder().decode(bytes.decode(resp.read()))
        print("--------------------------")
        print("---------GOOGLE----------")
        print("Hôtels dans " + quartier["properties"]["nom"] + " :")
        if jsonData["status"] == "OVER_QUERY_LIMIT":
            print("Nombre maximal de requêtes atteint. Réessayez plus tard")
            continue
        for hotel in jsonData["results"]:
            print("- " + hotel["name"] + " : (" + str(hotel["geometry"]["location"]["lat"]) + ', ' + str(hotel["geometry"]["location"]["lng"]) + ')')
        #quartier["location"] = jsonData["results"]["location"]
    else:
        print("Erreur requête : " + resp.status)

    # HERE API
    connection = client.HTTPSConnection("places.cit.api.here.com")
    connection.request("GET", "/places/v1/discover/search?" +
                         parse.urlencode({"at": str(centre["lon"]) + "," + str(centre["lat"]), "q": "hotel",
                                          "app_id": "YOUR_APP_ID", "app_code": "YOUR_APP_CODE"}), "",
                         {"Accept": "application/json"})
    # requete = "/places/v1/autosuggest/" + parse.urlencode({"at": str(centre["lon"]) + "," + str(centre["lat"]), "q": "hotel",
    #                                       "app_id": "YOUR_APP_ID", "app_code": "YOUR_APP_CODE"})
    # print(requete)
    resp = connection.getresponse()
    if resp.status == client.OK:
        jsonData = json.JSONDecoder().decode(bytes.decode(resp.read()))
        print("--------------------------")
        print("---------HERE-----------")
        print("Hôtels dans " + quartier["properties"]["nom"] + " :")
        for hotel in jsonData["results"]["items"]:
            print("- " + hotel["title"] + " : (" + str(hotel["position"][1]) + ', ' + str(hotel["position"][0]) + ')')
    else:
        print("Erreur requête : " + resp.status)
