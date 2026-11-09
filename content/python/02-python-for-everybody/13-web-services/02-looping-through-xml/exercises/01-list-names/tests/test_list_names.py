from solution import branch_names


def test_two():
    xml = "<library><branch><name>Central</name></branch><branch><name>Riverside</name></branch></library>"
    assert branch_names(xml) == ["Central", "Riverside"]


def test_empty():
    assert branch_names("<library></library>") == []


def test_order_kept():
    xml = "<library>" + "".join(f"<branch><name>{n}</name></branch>" for n in "zay") + "</library>"
    assert branch_names(xml) == ["z", "a", "y"]
