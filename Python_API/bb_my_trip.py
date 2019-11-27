import json
from Xm import *

# Lecture du fichier dans un dictionnaire
with open("trip.geojson") as f:
    trip = json.load(f)

# Préparation du document
xm = Xm()

# Première balise kml racine
main = xm.group('kml', {"xmlns": "http://www.opengis.net/kml/2.2"}, [])

# Balise Document
document = xm.group("Document", {}, [xm.text("name", {}, "A Walk in New York")])

# Balise Style stylePOIs
stylePOIs = xm.group("Style", {"id": "stylePOIs"}, [])
# Balise IconStyle
icon_style = xm.group("IconStyle", {}, [])
# Balise Icon
icon = xm.group("Icon", {}, [xm.text("href", {}, "http://maps.google.com/intl/en_us/mapfiles/ms/micons/yellow.png")])
# On ajoute la balise Icon à la balise IconStyle
xm.add(icon_style, icon)
xm.add(icon_style, xm.text("scale", {}, 1.4))
# On ajoute la balise IconStyle à la balise Style stylePOIs
xm.add(stylePOIs, icon_style)
# Balise LabelStyle
label_style = xm.group("LabelStyle", {}, [xm.text("color", {}, "ff4763ff"), xm.text("scale", {}, 0.7)])
# On ajoute la balise LabelStyle à la balise Style stylePOIs
xm.add(stylePOIs, label_style)
# On ajoute la balise Style stylePOIs à la balise Document
xm.add(document, stylePOIs)

# Balise Style stylePromenades
stylePromenades = xm.group("Style", {"id": "stylePromenades"}, [])
# Balise LineStyle
line_style = xm.group("LineStyle", {}, [xm.text("color", {}, "ff8cb4d2"), xm.text("width", {}, 5)])
# On ajoute la balise LineStyle à la balise Style stylePromenades
xm.add(stylePromenades, line_style)
# On ajoute la balise Style stylePromenades à la balise Document
xm.add(document, stylePromenades)

# Balise Folder Lieux visités
lieux_visites = xm.group("Folder", {}, [xm.text("name", {}, "Lieux visités"), xm.text("open", {}, 0)])
for poi in trip["features"]:
    if poi["geometry"]["type"] == "Point":
        # Balise Placemark
        placemark = xm.group('Placemark', {}, [xm.text('name', {}, poi["properties"]["Name"]), xm.text('styleUrl', {}, "#stylePOIs")])
        # Balise Point
        point = xm.group('Point', {}, [xm.text('coordinates', {}, str(poi["geometry"]["coordinates"][0]) + ','
                                               + str(poi["geometry"]["coordinates"][1]) + ','
                                               + str(poi["geometry"]["coordinates"][2]))])
        # On ajoute la balise Point à la balise Placemark
        xm.add(placemark, point)
        # On ajoute la balise Placemark à la balise Folder Lieux visités
        xm.add(lieux_visites, placemark)
# On ajoute la balise Folder Lieux visités à la balise Document
xm.add(document, lieux_visites)

# Balise Folder Promenades
promenades = xm.group("Folder", {}, [xm.text("name", {}, "Promenades"), xm.text("open", {}, 0)])
for poi in trip["features"]:
    if poi["geometry"]["type"] == "LineString":
        # Balise Placemark
        placemark = xm.group('Placemark', {}, [xm.text('name', {}, poi["properties"]["Name"]), xm.text('styleUrl', {}, "#stylePromenades")])
        coordinates = []
        for coord in poi["geometry"]["coordinates"]:
            point = []
            for i in coord:
                point.append(str(i))
            coordinates.append(','.join(point))
            str_line = ' '.join(coordinates)
        # Balise LineString
        line = xm.group('LineString', {}, [xm.text("tessellate", {}, 1),
                                           xm.text("coordinates", {}, str_line)])
        # On ajoute la balise LineString à la balise Placemark
        xm.add(placemark, line)
        # On ajoute la balise Placemark à la balise Folder Promenades
        xm.add(promenades, placemark)
# On ajoute la balise Folder Promenades à la balise Document
xm.add(document, promenades)
# On ajoute la balise Document à la balise kml racine
xm.add(main, document)
# Déclaration de la balise racine
xm.root(main)

print(xm.tostring())
# Export de l'arborescence vers un fichier KML
xm.tofile("trip.kml")