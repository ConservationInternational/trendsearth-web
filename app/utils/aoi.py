import json
import logging

from osgeo import ogr, gdal, osr
from marshmallow_dataclass import dataclass

logger = logging.getLogger(__name__)


def _get_bounding_box_geom(geom):
    (minX, maxX, minY, maxY) = geom.GetEnvelope()
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint_2D(minX, minY)
    ring.AddPoint_2D(maxX, minY)
    ring.AddPoint_2D(maxX, maxY)
    ring.AddPoint_2D(minX, maxY)
    ring.AddPoint_2D(minX, minY)
    poly_envelope = ogr.Geometry(ogr.wkbPolygon)
    poly_envelope.AddGeometry(ring)

    return poly_envelope


# TODO: Doesn't yet work on points
@dataclass
class AOI(object):
    geojson: dict

    @property
    def crs(self):
        return ogr.Open(
            json.dumps(
                self.geojson)).GetSpatialReference().ExportToWkt()

    def _get_unary_union(self):
        logging.debug('getting unary union')
        union = None
        for layer in ogr.Open(json.dumps(self.geojson)):
            for feature in layer:
                if not union:
                    union = feature.geometry().Clone()
                else:
                    union = union.Union(feature.geometry())
        return union

    def meridian_split(self, as_extent=False, out_format='geojson'):
        """
        Return list of bounding boxes in WGS84 as geojson or WKT
        Returns multiple geometries as needed to avoid having an extent
        crossing the 180th meridian
        """

        logging.debug('performing meridian split')
        if out_format not in ['geojson', 'wkt']:
            raise ValueError(f'Unrecognized out_format "{out_format}')
        unary_union = self._get_unary_union()

        hemi_e = ogr.CreateGeometryFromWkt(
            'POLYGON ((0 -90, 0 90, 180 90, 180 -90, 0 -90))')
        hemi_w = ogr.CreateGeometryFromWkt(
            'POLYGON ((-180 -90, -180 90, 0 90, 0 -90, -180 -90))')
        intersections = [
            hemi.Intersection(unary_union) for hemi in [hemi_e, hemi_w]
        ]

        logging.debug('making pieces')
        pieces = [
            i for i in intersections if not i.IsEmpty()
        ]
        pieces_extents = [_get_bounding_box_geom(i) for i in pieces]
        if as_extent:
            split_out = pieces_extents
            unsplit_out = [_get_bounding_box_geom(unary_union)]
        else:
            split_out = pieces
            unsplit_out = [unary_union]

        # Perform areal calculations on extents even if output is NOT extents,
        # so that meridian split gives consistent results (in terms of number
        # of pieces) regardless of whether requested output is original
        # polygons or extents
        pieces_extents_union = pieces_extents[0].Clone()
        for piece_extent in pieces_extents[1:]:
            pieces_extents_union = pieces_extents_union.Union(piece_extent)
        bounding_area_unsplit = _get_bounding_box_geom(
            pieces_extents_union).GetArea()
        bounding_area_split = sum(
            [piece_extent.GetArea() for piece_extent in pieces_extents]
        )

        logging.debug(
            f'len(pieces_extents): {len(pieces_extents)} '
            f'unary_union area {unary_union.GetArea()}, '
            f'bounding_area_unsplit: {bounding_area_unsplit}',
            f'bounding_area_split: {bounding_area_split}')

        if (
            (len(pieces) == 1) or
            (bounding_area_unsplit < 5 * bounding_area_split)
        ):
            # If there is no area in one of the hemispheres, return the
            # original layer, or extent of the original layer. Also return the
            # original layer (or extent) if the area of the combined pieces
            # from both hemispheres is not significantly smaller than that of
            # the original polygon.
            logger.info("AOI being processed in one piece "
                        "(does not appear to cross 180th meridian)")
            out = unsplit_out
        else:
            logger.info("AOI appears to cross 180th meridian "
                        "- splitting AOI into two geojsons.")
            out = split_out

        if out_format == 'geojson':
            return [json.loads(o.ExportToJson()) for o in out]
        elif out_format == 'wkt':
            return [o.ExportToWkt() for o in out]

    def get_aligned_output_bounds(self, f):
        geojsons = self.meridian_split(as_extent=True)

        if not geojsons:
            out = None

        else:
            out = []
            for geojson in geojsons:
                # Compute the pixel-aligned bounding box (slightly larger than
                # aoi).
                # Use this to set bounds in vrt files in order to keep the
                # pixels aligned with the chosen layer
                geom = ogr.CreateGeometryFromJson(str(geojson))
                (minx, maxx, miny, maxy) = geom.GetEnvelope()
                gt = gdal.Open(f).GetGeoTransform()
                left = minx - (minx - gt[0]) % gt[1]
                if left < -180:
                    left = -180
                right = maxx + (gt[1] - ((maxx - gt[0]) % gt[1]))
                if right > 180:
                    right = 180
                bottom = miny + (gt[5] - ((miny - gt[3]) % gt[5]))
                if bottom < -90:
                    bottom = -90
                top = maxy - (maxy - gt[3]) % gt[5]
                if top > 90:
                    top = 90
                out.append([left, bottom, right, top])

        return out

    def get_crs_wkt(self):
        # TODO fix this
        # return self.geojson.GetSpatialReference().ExportToWkt()
        return '''GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",
        6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,
        AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'''

    def bounding_box_gee_geojson(self):
        '''
        Returns list of bounding box geojsons.
        '''

        if self.datatype == 'polygon':
            return self.meridian_split()
        elif self.datatype == 'point':
            # TODO: Code this for OGR

            # If there is only on point, don't calculate an extent (extent of
            # one point is a box with sides equal to zero)
            n = 0

            for f in self.l.getFeatures():
                n += 1

                if n == 1:
                    # Save the first geometry in case it is needed later
                    # for a layer that only has one point in it
                    geom = f.geometry()

            if n == 1:
                logger.info('Layer only has one point')

                return [json.loads(geom.asJson())]
            else:
                logger.info('Layer has many points ({})'.format(n))

                return self.meridian_split()
        else:
            raise RuntimeError(
                f"Failed to process area of interest - unknown geometry "
                f"type: {self.geojson.GetGeometryType()}"
            )

    def calc_frac_overlap(self, in_geom):
        """
        Returns fraction of AOI that is overlapped by OGR geometry
        Used to calculate "within" with a tolerance
        """
        aoi_geom = ogr.CreateGeometryFromWkt(self.bounding_box_geom().asWkt())

        geom_area = aoi_geom.GetArea()

        if geom_area == 0:
            # Handle case of a point with zero area
            frac = aoi_geom.Within(in_geom)
        else:
            frac = aoi_geom.Intersection(in_geom).GetArea() / geom_area

        return frac

    def get_geojson(self, split=False):
        if split:
            out = {"type": "FeatureCollection", "features": []}
            out['features'].append(self.meridian_split(as_extent=False))
        else:
            out = self.geojson
        return out

    def transform(self, srid=3857):
        geom = ogr.Open()
        ds = ogr.Open(str(self.geojson))
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

        geojsondict = json.loads(str(self.geojson))
        for layer in ds:
            i = 0
            for feature in layer:
                geom = feature.geometry()
                geom.Transform(coordTrans)
                geojsondict["features"][i]["geometry"] = json.loads(
                    geom.ExportToJson())

        geojsondict["crs"] = crs

        return geojsondict
