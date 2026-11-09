"""Pipeline error tracking."""


class Pipeline:
    errors = []

    def __init__(self, name):
        self.name = name

    def record_error(self, msg):
        self.errors.append(f"{self.name}: {msg}")

    def failed(self):
        return bool(self.errors)
