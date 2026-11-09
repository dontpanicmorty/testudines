import xml.etree.ElementTree as ET


def parse_reading(xml_text):
    root = ET.fromstring(xml_text)
    temp = root.find("temp")
    return (root.get("sensor"), float(temp.text), temp.get("unit"))
