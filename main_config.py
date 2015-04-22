# -*- coding: utf-8 -*-
import os
import json

supported_ext_for_analysis = ['.jpg']

with open('json/name_dictionary.json', encoding='utf-8') as f:
    name_dictionary = json.load(f)


def get_name(name):
    try:
        return name_dictionary[name][language]
    except KeyError as e:
        print(e)
        return name

# Interface
language = 'ru'
img_long_edge = 500
main_bg = '#999999'
main_fg = '#000000'
canvas_bg = '#222222'

# External binary tools
exiftool = os.path.abspath('bin/exiftool.exe')
# FIXME: change path, when you are ready
object_detector = os.path.abspath('D:/Studies/_Graduation_thesis/Programming/C++/object_detection/Debug/object_detection.exe')

# Geocoders
yandex_geocoder = 'http://geocode-maps.yandex.ru/1.x/'
osm_geocoder = 'http://nominatim.openstreetmap.org/search/'

# Paths to JSON configs
cascades_json = 'json/cascades.json'
osm_types_and_classes_json = 'json/osm_types_and_classes.json'

#traces = main_config['traces']