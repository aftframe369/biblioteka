import csv
import urllib.request
import os

def read_csv():
    with urllib.request.urlopen('https://raw.githubusercontent.com/aftframe369/biblioteka_data/main/data.csv') as file:
        file = [l.decode('utf-8') for l in file.readlines()]
        reader = csv.reader(file)
        next(reader)
        for i in reader:
            yield i

class book:
    def __init__(self, id: int, title: str, author: str, amount: int, category: str):
        self.id = id
        self.title = title
        self.author = author
        self.amount = amount
        self.category = category

    def __repr__(self) -> str:
        return f'{self.id} | {self.title} | {self.author} | {self.amount} | {self.category}'


class biblioteka:
    def __init__(self):
        self.books = []

    def all(self):
        return self.books

    def load(self):
        for i in read_csv():
            self.books.append(book(int(i[0]), i[1], i[2], int(i[3]), i[4]))

    def where_id(self, id=0):
        for book in self.books:
            if book.id == int(id): return book

    def __iter__(self):
        for i in self.books:
            yield i


class kategoria:
    def __init__(self, id, cat, amount):
        self.cat_id = id
        self.category = cat
        self.amount = amount

    def __repr__(self) -> str:
        return f'{self.cat_id} | {self.category} | {self.amount}'


class kategorie:
    def __init__(self, biblioteka):
        self.kategorie = []
        self.kats = []
        for i in biblioteka:
            self.kats.append(i.category)
        self.kats = list(set(self.kats))
        self.kats.sort()
        for i, cat in enumerate(self.kats):
            self.kategorie.append(kategoria(i, cat, 0))
        for book in biblioteka:
            for cat in self.kategorie:
                if book.category == cat.category: cat.amount+=1

    def __iter__(self):
        for i in self.kategorie:
            yield i

if __name__ == '__main__':
    import os
    os.chdir('biblioteka/biblioteka')
    books = biblioteka()
    books.load()
    categories = kategorie(books)

    for i in categories:
        (print(i))

                


