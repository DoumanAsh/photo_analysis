# -*- coding: utf-8 -*-
import tracer as trace


@trace.enter
def convert_address_to_exiftool_format(address):
    d = dict(
        # Yandex kinds
        country="Country-PrimaryLocationName",
        province="Province-State",
        locality="City",
        area="Sub-location",
        district="Sub-location"
    )

    return d.get(address)


@trace.enter
def get_info_yandex(latitude, longitude):
    import requests
    import os
    import json
    from main_config import yandex_geocoder

    items = {}
    query = "{0}?format=json&geocode={1},{2}".format(yandex_geocoder, longitude, latitude)

    try:
        result = requests.get(query)
    except Exception as e:
        trace.error('Exception: {0}'.format(e))
        return items

    core_dic = json.loads(result.text)
    try:
        for feature_member in core_dic['response']['GeoObjectCollection']['featureMember']:
            try:
                kind = feature_member['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind']
                items[kind] = feature_member['GeoObject']['name']
            except KeyError as e:
                trace.warning("Invalid key: {0}".format(e))
    except KeyError as e:
        trace.warning("Invalid key: {0}".format(e))
        return items

    return items


@trace.enter
def get_info_osm(latitude, longitude):
    import requests
    import os
    import json
    from main_config import osm_geocoder

    keywords = []
    query = "{0}?format=json&q={1},{2}".format(osm_geocoder, latitude, longitude)

    try:
        result = requests.get(query)
    except Exception as e:
        trace.error('Exception: {0}'.format(e))
        return keywords
    core_dic = json.loads(result.text)

    object_class = core_dic[0]["class"]
    object_type = core_dic[0]["type"]

    keywords.append(core_dic[0]["display_name"].split(",")[0])
    keywords.extend(get_osm_keywords(object_class, object_type))
    return keywords


@trace.enter
def get_geo_tags_in_et_format(image_name):
    import sys
    import exif_jpeg as exif
    exif_gps = exif.get_exif_field(image_name, "GPSInfo")
    try:
        gps_info = exif.parse_gps_info(exif_gps, "dd") if exif_gps else None
    except KeyError:
        gps_info = None
    if not gps_info:
        return {}
    latitude = float(gps_info["latitude"][0])
    longitude = float(gps_info["longitude"][0])
    y_d = get_info_yandex(latitude, longitude)
    et_d = dict(keywords=[])
    for tag in y_d:
        et_key = convert_address_to_exiftool_format(tag)
        if et_key:
            et_d[et_key] = y_d[tag]
        else:
            et_d["keywords"].append(y_d[tag])
    et_d["keywords"].extend(get_info_osm(latitude, longitude))
    return et_d


def get_osm_keywords(object_class, object_type):
    import json
    from main_config import osm_types_and_classes
    with open(osm_types_and_classes, encoding='utf-8') as f:
        kw_dict = json.load(f)
    keywords = []
    try:
        keywords.extend(kw_dict[object_class][object_type])
    except KeyError:
        pass
    return keywords