from flask import Blueprint, render_template, request
from .models import kategorie, biblioteka
from random import sample
from . import search


#TODO: Change name to title in db
views = Blueprint('views', __name__)

@views.route('/')
def index():
    books = biblioteka.query.all()
    kats = kategorie.query.order_by(kategorie.category).all()
    rand_books = sample(books, 3)
    return render_template('index.html', books=books, kategorie=kats, rand_books=rand_books)

@views.route('/kategoria/<string:category>')
def category_page(category):
    books = biblioteka.query.filter_by(category=category).all()
    kats = kategorie.query.order_by(kategorie.category).all()
    if len(books) < 3: rand_books = books
    else: rand_books = sample(books, 6)
    return render_template('category.html', books = books, rand_books=rand_books, od=0, do=10, kategorie=kats)

@views.route('/book/<id>')
def book_page(id):
    book = biblioteka.query.filter_by(id=id).first()
    kats = kategorie.query.order_by(kategorie.category).all()
    return render_template('book.html', book = book, kategorie=kats)

@views.route('/search', methods=["POST"])
def search_page():
    kats = kategorie.query.order_by(kategorie.category).all()
    print(request.form['search'])
    ranked_by_title, ranked_by_authors, ranked_by_category = search(request.form['search'])
    return render_template('search.html', results=ranked_by_title, kategorie = kats, od=0, do=30)

@views.route('/book/lend-<id>')
def lend_book(id):
    kats = kategorie.query.order_by(kategorie.category).all()
    book = biblioteka.query.filter_by(id=id).first()
    return render_template('lend.html', kategorie=kats, book=book)