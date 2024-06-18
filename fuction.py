from models import session, User, Note, select
from datetime import datetime
import bcrypt, re

def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

def is_valid_password(password):
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def add_note_func(title, text, user):
    note = Note(title=title, text=text, creation_date=datetime.now(), user=user)
    session.add()
    session.commit()

    return note

def del_note_func(id):
    note = session.query(Note).filter(Note.id == id).first()
    session.delete(note)
    session.commit()
    
    return note

def add_user(email, password):
    user = User(email=email, password=hash_password(password))
    session.add(user)
    session.commit()

    return user

def del_user(id):
    user = session.query(User).filter(User.id == id).first()
    session.delete(user)
    session.commit()

    return user

def edit_note_title(id, title):
    note = session.query(Note).filter(Note.id == id).first()
    note.title = title
    session.commit()

    return note
    
def edit_note_text(id, text):
    note = session.query(Note).filter(Note.id == id).first()
    note.text = text
    session.commit()

    return note

def check_login(email, password):
    user = session.query(User).filter(User.email == email).first()
    return check_password(password, user.password.encode('utf-8'))

def check_email(email):
    user = session.query(User).filter(User.email == email).first()
    return True if user else False