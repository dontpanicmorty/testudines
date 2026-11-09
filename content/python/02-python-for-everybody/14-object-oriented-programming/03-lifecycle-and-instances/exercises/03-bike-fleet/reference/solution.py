class Bike:
    def __init__(self, bike_id):
        self.bike_id = bike_id
        self.rented = False


class Fleet:
    def __init__(self):
        self.bikes = {}

    def add(self, bike):
        self.bikes[bike.bike_id] = bike

    def rent(self, bike_id):
        bike = self.bikes.get(bike_id)
        if bike is None or bike.rented:
            return False
        bike.rented = True
        return True

    def bring_back(self, bike_id):
        bike = self.bikes.get(bike_id)
        if bike is None or not bike.rented:
            return False
        bike.rented = False
        return True

    def available(self):
        return sorted(i for i, b in self.bikes.items() if not b.rented)
