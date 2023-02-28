import sqlite3 as sql

con = sql.connect('/home/maciej/Programowanie/Web/instance/database.db')

cur = con.cursor()

def zmien_na_jak_w_zdaniu():
    b = cur.execute('SELECT * FROM biblioteka').fetchall()

    for record in b:
        print(record)
        cur.execute(f'UPDATE biblioteka SET kategoria = "{record[4].upper()[0]+record[4].lower()[1:]}" WHERE id={record[0]}')
        #print(f'STARE:{record[4]} NOWE: "{record[4].upper()[0]+record[4].lower()[1:]}"  id={record[0]}')
        con.commit()

def usun_kategorie():
    b = cur.execute('SELECT * FROM kategorie').fetchall()

    for record in b:
        a = cur.execute(f'SELECT kategoria FROM biblioteka WHERE kategoria="{record[1]}"').fetchall()
        if len(a) == 0: 
            cur.execute(f'DELETE FROM kategorie WHERE col_id={record[0]}')
            con.commit()

def zmien_na(list1, list2):
    for i, j in zip(list1, list2):
        pass

def policz_kategorie():
    for record in cur.execute('SELECT * FROM kategorie').fetchall():
        amount = int(len(cur.execute(f'SELECT * FROM biblioteka WHERE kategoria = "{record[1]}"').fetchall()))
        cur.execute(f'UPDATE kategorie SET amount={amount} WHERE col_id="{record[0]}"')
        con.commit()

def count_books_and_csv():
    print(len(cur.execute('SELECT * FROM biblioteka').fetchall()))
    with open('/home/maciej/Programowanie/Web/instance/spis.csv', 'r') as file:
        print(len(file.readlines()))

def print_database(name):
    a = cur.execute(f'SELECT * FROM {name}').fetchall()
    for i in a: print(a)

policz_kategorie()