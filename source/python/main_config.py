# -*- coding: utf-8 -*-
from os import path
from json import load as json_load

supported_ext_for_analysis = {'.jpg', '.jpeg'}
supported_image_ext = {'.jpg', '.jpeg', '.cr2'}

# Interface
language = 'ru'
top_level_padding = 5
min_preview_size = 150
max_preview_size = 750
main_bg = '#BBBBBB'
main_fg = '#000000'
btn_bg = '#DDDDDD'
btn_fg = '#000000'
canvas_bg = '#222222'

# External binary tools
exiftool = path.abspath('bin/exiftool.exe')
# FIXME: change path, when you are ready
object_detector = path.abspath('D:/Studies/_Graduation_thesis/Programming/C++/object_detection/Debug/object_detection.exe')

# Geocoders
yandex_geocoder = 'http://geocode-maps.yandex.ru/1.x/'
osm_geocoder = 'http://nominatim.openstreetmap.org/search/'

# Paths to JSON configs
cascades_json = 'json/cascades.json'
osm_types_and_classes_json = 'json/osm_types_and_classes.json'
settings_json = 'json/settings.json'

with open('json/name_dictionary.json', encoding='utf-8') as _f:
    name_dictionary = json_load(_f)

with open(settings_json, encoding='utf-8') as _f:
    settings = json_load(_f)

project_file = 'photo_project.json'


def get_name(name):
    try:
        return name_dictionary[name][language]
    except KeyError as e:
        print(e)
        return name
