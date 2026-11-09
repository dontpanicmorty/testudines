class Shape:
    def area(self):
        raise NotImplementedError("subclasses must define area")


class Rect(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rect):
    def __init__(self, side):
        super().__init__(side, side)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius * self.radius


def total_area(shapes):
    return round(sum(s.area() for s in shapes), 2)
