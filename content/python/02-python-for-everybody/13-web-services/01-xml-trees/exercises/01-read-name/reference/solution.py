import xml.etree.ElementTree as ET


def town_name(xml_text):
    root = ET.fromstring(xml_text)
    return root.find("name").text
