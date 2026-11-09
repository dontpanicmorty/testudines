class Session:
    def __init__(self, log, name):
        self.log = log
        self.name = name
        log.append(f"open {name}")

    def __del__(self):
        self.log.append(f"close {self.name}")
