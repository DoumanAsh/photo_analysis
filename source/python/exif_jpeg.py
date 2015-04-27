# -*- coding: utf-8 -*-
import tracer as trace

def get_all_exif(img_name):
    from PIL import Image
    from PIL.ExifTags import TAGS

    fields = {}
    i = Image.open(img_name)
    info = i._getexif()

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        fields[decoded] = value

    return fields


def get_exif_field(img_name, field):
    from PIL import Image
    from PIL.ExifTags import TAGS

    fields = {}
    i = Image.open(img_name)
    info = i._getexif()

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        fields[decoded] = value

    if field in fields.keys():
        return fields[field]
    else:
        return None


@trace.enter
def parse_gps_info(gps_info, coord_format="dd", signed=True):
    """
    Allowed coordinates formats:
    dms - degrees minutes seconds (40° 26′ 46″ N 79° 58′ 56″ W)
    ddm - degrees decimal minutes (40° 26.767′ N 79° 58.933′ W)
    dd  - decimal degrees (40.446° N 79.982° W)

    Signed:
    False - N40.446 W79.982; S40.446 E79.982
    True -  40.446 79.982; -40.446 -79.982
    """
    coordinates = dict(latitude="", longitude="", altitude="")

    if gps_info[18] != "WGS-84":
        print("Unsupported GPS-info standard: " + gps_info[18])
        return coordinates

    # Parse altitude
    if 6 in gps_info:
        sign = '-' if gps_info[5] == 1 else ''
        coordinates["altitude"] = sign + str(gps_info[6][0]/gps_info[6][1])

    # Parse latitude
    lat_symbol = gps_info[1]
    lat = gps_info[2]
    lat_degree = int(lat[0][0]/lat[0][1])
    if lat[1][0] == 0:
        lat_minutes = int(60*(lat[0][0] - lat_degree*lat[0][1])/lat[0][1])
        lat_seconds = 3600*(lat[0][0] - lat_degree*lat[0][1] - lat_minutes*lat[0][1])/lat[0][1]
    else:
        lat_minutes = int(lat[1][0]/lat[1][1])
        if lat[2][0] == 0:
            lat_seconds = 60*(lat[1][0] - lat_minutes*lat[1][1])/lat[1][1]
        else:
            lat_seconds = lat[2][0]/lat[2][1]

    # Parse longitude
    lon_symbol = gps_info[3]
    lon = gps_info[4]
    lon_degree = int(gps_info[4][0][0]/lon[0][1])
    if lon[1][0] == 0:
        lon_minutes = int(60*(lon[0][0] - lon_degree*lon[0][1])/lon[0][1])
        lon_seconds = 3600*(lon[0][0] - lon_degree*lon[0][1] - lon_minutes*lon[0][1])/lon[0][1]
    else:
        lon_minutes = int(lon[1][0]/lon[1][1])
        if lon[2][0] == 0:
            lon_seconds = 60*(lon[1][0] - lon_minutes*lon[1][1])/lon[1][1]
        else:
            lon_seconds = lon[2][0]/lon[2][1]

    if coord_format == "dd":
        coordinates["latitude"] = [str(lat_degree + lat_minutes/60 + lat_seconds/3600)]
        coordinates["longitude"] = [str(lon_degree + lon_minutes/60 + lon_seconds/3600)]
    elif coord_format == "ddm":
        coordinates["latitude"] = [str(lat_degree), str(lat_minutes + lat_seconds/60)]
        coordinates["longitude"] = [str(lon_degree), str(lon_minutes + lon_seconds/60)]
    elif coord_format == "dms":
        coordinates["latitude"] = [str(lat_degree), str(lat_minutes), str(lat_seconds)]
        coordinates["longitude"] = [str(lon_degree), str(lon_minutes), str(lon_seconds)]
    else:
        print("Incorrect format: " + format)
        return coordinates

    if signed:
        negative_sign = ["S", "W"]

        sign = '+' if not lat_symbol in negative_sign else '-'

        coordinates["latitude"][0] = "".join((sign, coordinates["latitude"][0]))

        sign = '+' if not lon_symbol in negative_sign else '-'
        coordinates["longitude"][0] = "".join((sign, coordinates["longitude"][0]))
    else:
        coordinates["latitude"].extend(lat_symbol)
        coordinates["longitude"].extend(lon_symbol)

    return coordinates
