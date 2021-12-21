from osgeo import ogr, osr
import json

geojsonfile = '''{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[34.54999385451819, -0.449578838201173], [34.7299938545182, -0.449578838201173], [34.7299938545182, -0.269578838201173], [34.54999385451819, -0.269578838201173], [34.54999385451819, -0.449578838201173]]]}}], "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}}'''
srid = 3857
ds = ogr.Open(geojsonfile)
layer = ds.GetLayer()
inSpatialRef = layer.GetSpatialRef()

# output SpatialReference
outSpatialRef = osr.SpatialReference()
outSpatialRef.ImportFromEPSG(srid)

# create the CoordinateTransformation
coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

union = None
crs = {'type': 'name', 'properties': {
    'name': 'urn:ogc:def:crs:EPSG::{}'.format(srid)}}

geojsonfile = json.loads(geojsonfile)
for layer in ds:
    i = 0
    for feature in layer:
        geom = feature.geometry()
        geom.Transform(coordTrans)
        geojsonfile["features"][i]["geometry"] = json.loads(
            geom.ExportToJson())

geojsonfile["crs"] = crs

print(geojsonfile)
