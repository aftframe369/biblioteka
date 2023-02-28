from . import db


class biblioteka(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('tytul', db.String(50))
    author = db.Column('autor', db.String(20))
    amount = db.Column('ilosc', db.Integer)
    category = db.Column('kategoria', db.String(20), db.ForeignKey('kategorie.category'))
    
    def __repr__(self):
        return f'<Książka {self.name} {self.author}>'


class kategorie(db.Model):
    cat_id = db.Column('col_id', db.Integer, primary_key=True)
    category = db.Column(db.String(20), unique=True)
    amount = db.Column(db.SmallInteger)

    def __repr__(self) -> str:
        return f'{self.category}'