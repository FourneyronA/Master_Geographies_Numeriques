#!/usr/bin/env python3

import json

data = json.load(open("trip.geojson"))

#
# Version Yattag
#

from yattag import Doc, indent

doc, tag, text, line = Doc().ttl()
doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
with tag('places'):
    for feature in data["features"]:
        if feature["geometry"]["type"] == "Point":
            line("poi", feature["properties"]["Name"], description='')

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
        content.append(xm.text("poi", {'description' : ''}, feature["properties"]["Name"]))
main = xm.group('places', {}, content)
xm.root(main)
xm.tofile('xm.xml')