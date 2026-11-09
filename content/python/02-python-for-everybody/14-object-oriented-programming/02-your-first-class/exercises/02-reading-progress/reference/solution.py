class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        self.page = 0

    def read(self, n):
        self.page = min(self.pages, self.page + n)

    def pages_left(self):
        return self.pages - self.page

    def percent(self):
        return round(100 * self.page / self.pages)

    def __str__(self):
        return f"{self.title} ({self.page}/{self.pages})"
