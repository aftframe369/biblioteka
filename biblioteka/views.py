from flask import Blueprint, render_template, request
from .models import kategorie, biblioteka
from random import sample
from . import search
from time import gmtime, time, strftime

# database loading
books = biblioteka()
last_updated = time()
books.load()
kats = kategorie(books)

views = Blueprint('views', __name__)

def update_database():
    # update database if more than an hour from last update
    global last_updated
    if time() - last_updated > 3600:
        books.load()
        print(f'database updated after {time() - last_updated:.2f}s')
        last_updated = time()


@views.route('/')
def index():
    update_database()
    rand_books = sample(list(books), 3)
    return render_template('index.html', books=books, kategorie=kats, rand_books=rand_books)


@views.route('/O_nas')
def o_nas():
    rand_books = sample(list(books), 3)
    return render_template('o_nas.html', books=books, kategorie=kats, rand_books=rand_books)


@views.route('/artysci_hufca')
def artysci():
    rand_books = sample(list(books), 3)
    return render_template('artysci.html', books=books, kategorie=kats, rand_books=rand_books)


@views.route('/kategoria/<string:category>-<int:page>')
def category_page_n(category, page):
    print(category)
    books_kats = [i for i in books if i.category == category]
    books_kats.sort(key=lambda d: d.title)
    print(books_kats)
    print(request.form)

    if len(books_kats) < 3:
        rand_books = books_kats
    else:
        rand_books = sample(books_kats, 3)

    if page != 109:
        per_page = 20
        ten_books = books_kats[page*per_page:(page+1)*per_page]
    else:
        per_page = 0
        ten_books = books_kats

    return render_template('category.html',
                           books=ten_books,
                           rand_books=rand_books,
                           kategorie=kats,
                           n=page,
                           amount_in_kat=kats.where_category(category).amount,
                           per_page=per_page)


@views.route('/book/<id>')
def book_page(id):
    return render_template('book.html', book=books.where_id(id), kategorie=kats)


@views.route('/search', methods=["POST"])
def search_page():
    update_database()
    query = request.form['search']
    ranked_by_title, ranked_by_authors, ranked_by_category = search(
        query, books)
    ranked_by_title_good = filter(lambda d: d['title'] > 0.5, ranked_by_title)
    ranked_by_title_bad = filter(
        lambda d: 0.35 < d['title'] <= 0.5, ranked_by_title)
    return render_template('search.html',
                           results_good=[i['book'] for i in ranked_by_title_good],
                           results_bad=[i['book'] for i in ranked_by_title_bad],
                           kategorie=kats,
                           query=query)


@views.route('/book/lend-<id>')
def lend_book(id):
    return render_template('lend.html', kategorie=kats, book=books.where_id(id))
