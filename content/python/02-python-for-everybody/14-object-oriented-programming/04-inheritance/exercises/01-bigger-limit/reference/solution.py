class Member:
    def __init__(self, name):
        self.name = name

    def loan_limit(self):
        return 3

    def summary(self):
        return f"{self.name}: {self.loan_limit()}"


class Student(Member):
    def loan_limit(self):
        return 5


class Staff(Member):
    def loan_limit(self):
        return 10
