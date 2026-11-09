import xml.etree.ElementTree as ET


def field_or_default(xml_text, tag, default):
    root = ET.fromstring(xml_text)
    child = root.find(tag)
    if child is None or child.text is None:
        return default
    return child.text
