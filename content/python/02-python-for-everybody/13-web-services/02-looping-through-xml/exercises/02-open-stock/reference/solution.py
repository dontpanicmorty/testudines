import xml.etree.ElementTree as ET


def open_bikes(xml_text):
    root = ET.fromstring(xml_text)
    total = 0
    for st in root.findall("station"):
        if st.get("status") == "open":
            total += int(st.find("bikes").text)
    return total
