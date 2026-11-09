import pytest

from solution import Circle, Rect, Shape, Square, total_area


def test_example():
    assert total_area([Rect(2, 3), Square(2)]) == 10


def test_circle_rounding():
    assert total_area([Circle(1)]) == 3.14
    assert total_area([Circle(2)]) == 12.57


def test_empty():
    assert total_area([]) == 0


def test_base_refuses():
    with pytest.raises(NotImplementedError):
        Shape().area()


def test_hierarchy():
    assert issubclass(Square, Rect)
    assert isinstance(Square(1), Shape)
    assert Square(3).area() == 9


def test_mixed():
    assert total_area([Square(1), Circle(1), Rect(1, 2)]) == 6.14
