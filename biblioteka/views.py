from flask import Blueprint, render_template, request
from .models import kategorie, biblioteka
from random import sample
from .search import search
from . import send_book_request
from time import time
from urllib.parse import unquote

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

    books_carouzel = sample(list(books), 3)
    return render_template('index.html', books=books, kategorie=kats, rand_books=books_carouzel)


@views.route('/O_nas')
def o_nas():
    return render_template('o_nas.html', books=books, kategorie=kats)


@views.route('/artysci_hufca')
def artysci():
    return render_template('artysci.html', books=books, kategorie=kats)


@views.route('/kategoria/<string:category>-<int:page>')
def category_page_n(category, page):
    print(unquote(category))

    """select all books that  have category == category from request, 
       unquote() changes %xx to utf-8 characters for comparison of categories
       with polish characters and spaces"""    
    books_kats = [i for i in books if i.category == unquote(category)]
    books_kats.sort(key=lambda d: d.title)

    """ if less than 3 books in category show them all in carouzel
        else sample 3 random books """
    if len(books_kats) < 3:
        books_carouzel = books_kats
    else:
        books_carouzel = sample(books_kats, 3)

    """ code 109 is a totally random, big number, 
    if user clicks 'show all' will be redirected to /'cat-109' 
    and all books in category will be listed """
    if page != 109:
        per_page = 20
        ten_books = books_kats[page*per_page:(page+1)*per_page]
    else:
        per_page = 0
        ten_books = books_kats

    return render_template('category.html',
                           books=ten_books,
                           rand_books=books_carouzel,
                           kategorie=kats,
                           n=page,
                           amount_in_kat=kats.where_category(category).amount,
                           per_page=per_page)


@views.route('/book/<id>')
def book_page(id):
    """ render information page for a single book """
    return render_template('book.html', book=books.where_id(id), kategorie=kats)


@views.route('/search', methods=["POST"])
def search_page():
    update_database()

    query = request.form['search']
    search_in = request.form['select_search']

    ranked_by_title, ranked_by_authors, ranked_by_category = search(query, books)
    
    """ split search results to those above and those below 0.5 relevance """
    print(search_in)
    if search_in == "title":
        results = ranked_by_title
    elif search_in == 'author':
        results = ranked_by_authors
    else: raise(KeyError)

    results_good = filter(lambda d: d[search_in] > 0.5, results)
    results_mediocore = filter(lambda d: 0.35 < d[search_in] <= 0.5, results)

    return render_template('search.html',
                           results_good=[i['book'] for i in results_good],
                           results_bad=[i['book'] for i in results_mediocore],
                           kategorie=kats,
                           query=query)


@views.route('/book/lend-<int:id>', methods=['GET','POST'])
def lend_book(id):
    form_success = False
    if request.method == 'POST':
        book = books.where_id(int(id))
        person = {
            'name': request.form['name'],
            'tribe': request.form['tribe'],
            'numer_ewidencji': request.form['numer_ewidencji'],
            'text': request.form['text_area'],
            'phone': request.form['phone']

        }
        send_book_request.send(book, person, 'zmaówienie')
        form_success = True


    return render_template('lend.html', kategorie=kats, book=books.where_id(id), form_success=form_success)

@views.route('/zaproponuj', methods=['GET','POST'])
def proposition():
    form_success = False

    if request.method == 'POST':
        book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'available': request.form['available'],
            'why': request.form['why'],

        }
        person = {
            'name': request.form['name'],
            'tribe': request.form['tribe'],
            'numer_ewidencji': request.form['numer_ewidencji'],
            'phone': request.form['phone'],
            'text': request.form['text_area']
        }
        send_book_request.send(book, person, 'propozycja')
        form_success = True
    return render_template('proposition.html', kategorie=kats, form_success=form_success)


@views.route('/polityka_prywatnosci')
def polityka_prywatnosci():
    return render_template('polityka_prywatnosci.html', kategorie=kats)
