# -*- coding: utf-8 -*-
from os import path
from json import load as json_load
from re import compile as re_compile

supported_ext_for_analysis = {'.jpg', '.jpeg'}
supported_image_ext = {'.jpg', '.jpeg', '.cr2'}
xmp_ext = '.xmp'

# Interface
top_level_padding = 5
min_preview_size = 150
max_preview_size = 750
main_bg = '#DCDCDC'
main_fg = '#000000'
btn_bg = '#FFFFFF'
btn_fg = '#000000'
canvas_bg = '#222222'

# External binary tools
exiftool = path.abspath('bin/exiftool.exe')
iptc_address_tags = {"Country-PrimaryLocationName", "Province-State", "City", "Sub-location"}
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
language = settings['language']
project_file = 'photo_project.json'

dir_source = 'Source'
dir_fullsize = 'Fullsize'
dir_monitor = 'Monitor'
dir_web = 'Web'
dir_panorama = 'Panorama'
dir_layered = 'Layered'

# Regex to find date/time in filename basing on pattern. Don't check limits for the numbers here.
dt_in_fn_regex = re_compile(".*(\d\d\d\d\-\d\d\-\d\d_\d\d\-\d\d\-\d\d).*")


def get_name(name):
    try:
        return name_dictionary[name][language]
    except KeyError as e:
        print(e)
        return name
