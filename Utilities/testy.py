from biblioteka import create_app
from biblioteka.models import kategorie, biblioteka
from random import randint


app = create_app()

with app.app_context():
    if __name__ == '__main__':
        kats = kategorie.query.all()
        print([str(kat) for kat in kats])
        data = biblioteka.query.filter_by(category=str(kats[randint(2, len(kats))])).all()
        print(data[0].title)
