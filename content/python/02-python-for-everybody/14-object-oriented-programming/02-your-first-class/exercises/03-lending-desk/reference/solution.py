class LendingDesk:
    def __init__(self):
        self.loans = {}

    def lend(self, title, member):
        if title in self.loans:
            return False
        self.loans[title] = member
        return True

    def give_back(self, title):
        if title not in self.loans:
            return False
        del self.loans[title]
        return True

    def titles_for(self, member):
        return sorted(t for t, m in self.loans.items() if m == member)

    def on_loan_count(self):
        return len(self.loans)
