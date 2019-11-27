#!/usr/bin/env python3

import json

data = json.load(open("trip.geojson"))

#
# Version Yattag
#

from yattag import Doc, indent

doc, tag, text, line = Doc().ttl()
doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
with tag('tourist_info'):
    for feature in data["features"]:
        if feature["geometry"]["type"] == "Point":
            with tag('visited_places', name = feature["properties"]["Name"], description = ''):
                line('latitude', feature["geometry"]["coordinates"][1])
                line('longitude', feature["geometry"]["coordinates"][0])
        if feature["geometry"]["type"] == "LineString":
            with tag('walk', name = feature["properties"]["Name"], description = ''):
                for point in feature["geometry"]["coordinates"]:
                    line('point', '%s,%s'%(point[1], point[0]))
            
file = open("yattag.xml", "w")
file.write(indent(doc.getvalue()))
file.close()

#
# Version Xm
#

from Xm import *

xm = Xm()
content = []
for feature in data["features"]:
    if feature["geometry"]["type"] == "Point":
        visited_place = xm.group('visited_place', {'name' : feature["properties"]["Name"], 'description' : ''}, [
            xm.text('latitude', {}, feature["geometry"]["coordinates"][1]),
            xm.text('longitude', {}, feature["geometry"]["coordinates"][0])
        ])
        content.append(visited_place)
    if feature["geometry"]["type"] == "LineString":
        points = []
        for point in feature["geometry"]["coordinates"]:
            points.append(xm.text('point', {}, '%s,%s'%(point[1], point[0])))
        walk = xm.group('walk', {'name' : feature["properties"]["Name"], 'description' : ''}, points)
        content.append(walk)
main = xm.group('tourist_info', {}, content)
xm.root(main)
xm.tofile('xm.xml')
