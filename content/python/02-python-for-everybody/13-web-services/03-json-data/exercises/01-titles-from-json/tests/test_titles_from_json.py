from solution import book_titles


def test_two():
    text = '{"shelf": "Maps", "books": [{"title": "Tide Tables", "year": 1999}, {"title": "Moss and Stone", "year": 2011}]}'
    assert book_titles(text) == ["Tide Tables", "Moss and Stone"]


def test_empty_shelf():
    assert book_titles('{"shelf": "Empty", "books": []}') == []


def test_unicode_title():
    assert book_titles('{"books": [{"title": "Café Nights"}]}') == ["Café Nights"]
