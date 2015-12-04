from sys import argv
from json import loads as json_loads
from json import load as json_load
import tracer as trace
import exif_jpeg as exif
from main_config import osm_types_and_classes_json, yandex_geocoder, osm_geocoder
from requests import get as request_get
from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException

# Yandex kinds
ADDR_TO_IPTC_FORMAT = {"country"  : "Country-PrimaryLocationName",
                       "province" : "Province-State",
                       "locality" : "City",
                       "area"     : "Sub-location",
                       "district" : "Sub-location"}

@trace.enter
def get_info_yandex(latitude, longitude):
    items = {}
    query = "{0}?format=json&geocode={1},{2}".format(yandex_geocoder, longitude, latitude)

    try:
        result = request_get(query)
    except ConnectionError as errno:
        trace.error(" ".join(("Connection error:", str(errno))))
        return items
    except Timeout as errno:
        trace.error(" ".join(("Connection timeoute exceed:", str(errno))))
        return items
    except HTTPError as errno:
        trace.error(" ".join(("Invalid HTTP response:", str(errno))))
        return items
    except RequestException as errno:
        trace.error('Exception: {0}'.format(errno))
        return items

    core_dic = json_loads(result.text)
    try:
        for feature_member in core_dic['response']['GeoObjectCollection']['featureMember']:
            try:
                kind = feature_member['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind']
                items[kind] = feature_member['GeoObject']['name']
            except KeyError as errno:
                trace.warning("Invalid key: {0}".format(errno))
    except KeyError as errno:
        trace.warning("Invalid key: {0}".format(errno))
        return items

    return items

@trace.enter
def get_info_osm(latitude, longitude):
    keywords = []
    query = "{0}?format=json&q={1},{2}".format(osm_geocoder, latitude, longitude)

    try:
        result = request_get(query)
    except ConnectionError as errno:
        trace.error(" ".join(("Connection error:", str(errno))))
        return keywords
    except Timeout as errno:
        trace.error(" ".join(("Connection timeoute exceed:", str(errno))))
        return keywords
    except HTTPError as errno:
        trace.error(" ".join(("Invalid HTTP response:", str(errno))))
        return keywords
    except RequestException as errno:
        trace.error('Exception: {0}'.format(errno))
        return keywords

    core_dic = json_loads(result.text)

    object_class = core_dic[0]["class"]
    object_type = core_dic[0]["type"]

    keywords.append(core_dic[0]["display_name"].split(",")[0])
    keywords.extend(get_osm_keywords(object_class, object_type))
    return keywords


@trace.enter
def get_geo_tags_in_iptc_format(image):
    exif_gps = exif.get_exif_field(image, "GPSInfo")
    try:
        gps_info = exif.parse_gps_info(exif_gps, "dd") if exif_gps else None
    except KeyError:
        gps_info = None
    if not gps_info:
        return {}

    latitude = float(gps_info["latitude"][0])
    longitude = float(gps_info["longitude"][0])

    trace.debug("GPS-coordinates of {0}: lat {1}; lon {2}".format(image, latitude, longitude))

    y_d = get_info_yandex(latitude, longitude)
    iptc_d = dict(keywords=[])

    for tag in y_d:
        iptc_key = ADDR_TO_IPTC_FORMAT[tag]
        if iptc_key:
            iptc_d[iptc_key] = y_d[tag]
        else:
            iptc_d["keywords"].append(y_d[tag])

    iptc_d["keywords"].extend(get_info_osm(latitude, longitude))
    return iptc_d


def get_osm_keywords(object_class, object_type):
    with open(osm_types_and_classes_json, encoding='utf-8') as json_file:
        kw_dict = json_load(json_file)

    keywords = []
    try:
        keywords.extend(kw_dict[object_class][object_type])
    except KeyError:
        pass

    return keywords

if __name__ == "__main__":
    geo_tags = get_geo_tags_in_iptc_format(argv[1])
    print("Results:")
    if geo_tags:
        for item in geo_tags:
            print("{0}: {1}".format(item, geo_tags[item]))
    else:
        print("geo-info not found")
