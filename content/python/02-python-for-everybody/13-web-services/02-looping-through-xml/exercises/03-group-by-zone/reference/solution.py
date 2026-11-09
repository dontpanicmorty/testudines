import xml.etree.ElementTree as ET


def stations_by_zone(xml_text):
    root = ET.fromstring(xml_text)
    result = {}
    for zone in root.findall("zone"):
        result[zone.get("name")] = [s.text for s in zone.findall("station")]
    return result
