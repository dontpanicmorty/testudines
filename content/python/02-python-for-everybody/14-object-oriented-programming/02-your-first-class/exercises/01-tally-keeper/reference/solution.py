class Tally:
    def __init__(self):
        self.count = 0

    def add(self, n=1):
        self.count += n

    def reset(self):
        self.count = 0
