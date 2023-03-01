from flask import Blueprint, render_template, request
from .models import kategorie, biblioteka
from random import sample
from . import search

books = biblioteka()
books.load()

kats = kategorie(books)


views = Blueprint('views', __name__)

@views.route('/')
def index():

    rand_books = sample(list(books), 3)
    return render_template('index.html', books=books, kategorie=kats, rand_books=rand_books)

@views.route('/kategoria/<string:category>')
def category_page(category):
    print(category)
    if category in kats.kats:
        books_kats = [i for i in books if i.category==category]
        print(books_kats    )
        if len(books_kats) < 3: rand_books = books_kats
        else: rand_books = sample(books_kats, 3)
        return render_template('category.html', books = books_kats, rand_books=rand_books, od=0, do=10, kategorie=kats)
    return index()


@views.route('/book/<id>')
def book_page(id):
    return render_template('book.html', book = books.where_id(id), kategorie=kats)

@views.route('/search', methods=["POST"])
def search_page():
    print(request.form['search'])
    ranked_by_title, ranked_by_authors, ranked_by_category = search(request.form['search'], books)
    return render_template('search.html', results=ranked_by_title, kategorie = kats, od=0, do=30)

@views.route('/book/lend-<id>')
def lend_book(id):
    return render_template('lend.html', kategorie=kats, book=books.where_id(id))