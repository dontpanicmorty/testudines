import xml.etree.ElementTree as ET


def branch_names(xml_text):
    root = ET.fromstring(xml_text)
    return [b.find("name").text for b in root.findall("branch")]
