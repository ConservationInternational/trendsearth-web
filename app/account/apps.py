import logging
import os
import json
from django.apps import AppConfig
from django.db import connection


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from utils.util import dictfetchall
        log = logging.getLogger(self.label)

        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from script")
                records = dictfetchall(cursor)
                if len(records) < 1:
                    cursor.execute(open(os.path.dirname(
                        os.path.abspath(__file__))
                        + "/configs/populate.sql").read())

                    # countries
                    filepath = os.path.dirname(
                        os.path.abspath(
                            __file__)) + "/configs/admin_bounds/admin_bounds_key.json"
                    countries = json.load(open(filepath))
                    for key, country in countries.items():
                        querystr = """INSERT INTO country(code, name, crs, wrap)
                         VALUES (%s, %s, %s, %s) RETURNING id;"""
                        values = (country.get("code"), key, int(
                            country.get("crs").split(":")[1]), country.get("wrap"))
                        cursor.execute(querystr, values)
                        countryid = dictfetchall(cursor)[0]["id"]
                        for key, province in country.get("admin1").items():
                            querystr = """INSERT INTO region(code, name,
                            country_id) VALUES (%s, %s, %s);"""
                            values = (province.get("code"), key, countryid)
                            cursor.execute(querystr, values)

                    # cities
                    filepath = os.path.dirname(os.path.abspath(
                        __file__)) + "/configs/admin_bounds/cities.json"
                    countries = json.load(open(filepath))
                    for abbrev, val in countries.items():
                        querystr = "SELECT id FROM country WHERE code = '{}'"\
                            .format(abbrev)
                        cursor.execute(querystr)
                        record = dictfetchall(cursor)[0]
                        countryid = record.get("id")
                        for key, city in val.items():
                            region_name = city.get("ADM1NAME")
                            geojson = json.dumps(
                                city.get("geojson").get("geometry"))
                            name_de = city.get("name_de")
                            name_en = city.get("name_en")
                            name_es = city.get("name_es")
                            name_fr = city.get("name_fr")
                            name_pt = city.get("name_pt")
                            name_ru = city.get("name_ru")
                            name_zh = city.get("name_zh")
                            querystr = """INSERT INTO cities(code, region_name,
                                        country_id, name_de, name_en, name_es,
                                            name_fr,
                                            name_pt, name_ru, name_zh, geom)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s,
                                            %s, %s, %s,
                                            ST_SetSRID(ST_GeomFromGeoJSON(%s),
                                            4326)) RETURNING id;"""
                            values = (key, region_name, countryid, name_de,
                                      name_en,
                                      name_es, name_fr, name_pt, name_ru, name_zh,
                                      geojson)
                            cursor.execute(querystr, values)

                    querystr = "SELECT id, code FROM country"
                    cursor.execute(querystr)
                    records = dictfetchall(cursor)
                    for record in records:
                        filepath = os.path.dirname(
                            os.path.abspath(__file__))
                        + "/configs/admin_bounds/admin_bounds_polys_{country}"\
                            ".json/admin_bounds_polys_{country}.json".format(
                                country=record.get("code"))
                        country = json.load(open(filepath))
                        querystr = "UPDATE country SET geom = ST_GeomFromGeoJSON('{}') "\
                            "WHERE id={}".format(
                                json.dumps(country.get(
                                    "geojson").get("geometry")),
                                record.get("id"))
                        cursor.execute(querystr)
                        print(querystr)
                        for key, value in country.get("admin1").items():
                            querystr = "UPDATE region SET geom = ST_GeomFromGeoJSON('{}')"\
                                " WHERE code='{}' AND country_id={}".format(
                                    json.dumps(
                                        value.get("geojson").get("geometry")),
                                    key, record.get("id"))
                            cursor.execute(querystr)
        except Exception as e:
            log.warn(e)
            log.warn(
                "Found an error when populating the database"
            )
