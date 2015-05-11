import json
import exiftool as et

iptc_address_tags = {"Country-PrimaryLocationName", "Province-State", "City", "Sub-location"}
photo = "D:/test_image.jpg"
iptc = et.get_data_from_image(photo, "-iptc:all")["IPTC"]
address = []
keywords = []
for key, item in iptc.items():
    if key == "Keywords":
        keywords.extend(item)
    elif key in iptc_address_tags:
        address.append(item)
print(keywords)
print(address)