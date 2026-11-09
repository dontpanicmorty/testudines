class Vehicle:
    def __init__(self, name, wheels):
        self.name = name
        self.wheels = wheels

    def describe(self):
        return f"{self.name} with {self.wheels} wheels"


class Trike(Vehicle):
    def __init__(self, name):
        super().__init__(name, 3)
        self.bell = True

    def describe(self):
        return super().describe() + " and a bell"
