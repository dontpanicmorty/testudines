from solution import town_name


def test_basic():
    assert town_name("<town><name>Larkfield</name><pop>900</pop></town>") == "Larkfield"


def test_name_not_first():
    assert town_name("<town><pop>5</pop><name>Oakby</name></town>") == "Oakby"


def test_whitespace_layout():
    xml = """<town>
      <name>Thistle End</name>
    </town>"""
    assert town_name(xml) == "Thistle End"


def test_name_with_spaces_inside():
    assert town_name("<town><name>Port of Dunmere</name></town>") == "Port of Dunmere"
