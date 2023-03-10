import smtplib
import ssl
from email.message import EmailMessage
from email.headerregistry import Address
from os import environ

passw = 'mcneetkykilaaxis'
passw = environ['MAIL_KEY']


def send(book, person_info, type):

    msg = EmailMessage()
    msg['Subject'] = f"{type} - {book}"
    msg['From'] = Address(f"{person_info['name']}", "mariuszkisling", 'gmail.com')
    msg['To'] = (
        Address("maciej glinski", "maciej.glinski+zamowienia", "zhp.net.pl"), 
        Address('asia pająk','joanna.pajak+zamowienia', 'zhp.net.pl')
        )

    if type=='zamówienie':
        msg.set_content(
                        f"""jestem {person_info['name']}
środowisko: {person_info['tribe']}
mój numer ewidencji: {person_info['numer_ewidencji']}.
tel/email: {person_info['phone']}

Chcę zamówić książkę 
id: {book.id}    
tytuł: {book.title}    
autor: {book.author}    
z kategorii: {book.category}    

{person_info['text']}

mail wygenerowany automatycznie ze strony biblioteka.vercell.app"""
        )
    
    elif type == 'propozycja':
        msg.set_content(
                        f"""jestem {person_info['name']}
środowisko: {person_info['tribe']}
mój numer ewidencji: {person_info['numer_ewidencji']}.
tel/email: {person_info['phone']}

Chcę zamówić książkę 
tytuł: {book['title']}    
autor: {book['author']} 
uzasadnienie: {book['why']}
dostępną w?: {book['available']}   

{person_info['text']}

mail wygenerowany automatycznie ze strony biblioteka.vercell.app"""
        )

    # Send the message via local SMTP s.
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        context = ssl.create_default_context()
        try:
            s.ehlo()  # check connection
            s.starttls(context=context)  # Secure the connection
            s.ehlo()  # check connection
            s.login('mariuszkisling@gmail.com', passw)
            s.send_message(msg)
        except:
            print('ojoj, nie udało się wysłać mejla')


if __name__ == '__main__':
    #will not wor, must insert real book object and person info object
    send('emilia kulczyk prus','maciuś i asiunia', 'zamówienie')