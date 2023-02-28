from biblioteka import db, create_app
from biblioteka.models import biblioteka
import csv

app = create_app()

with app.app_context():
    with open('instance/spis.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for i in reader:
            ksiazka = biblioteka(name=i[0], author=i[1], amount=int(i[2]), category=i[3])
            print(ksiazka)
            db.session.add(ksiazka)
    db.session.commit()
    biblioteka.query.all()