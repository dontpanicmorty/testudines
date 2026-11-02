"""A minimal shopping cart."""


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, sku, qty=1):
        self.items[sku] = self.items.get(sku, 0) + qty

    def remove(self, sku):
        del self.items[sku]

    def count(self):
        return sum(self.items.values())
