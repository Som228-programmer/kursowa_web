from flask import Flask, render_template, redirect, request, url_for
from fuction import *

user_email = None

app = Flask(__name__)

@app.route('/')
def main():
    global user_email
    if user_email is None:
        return redirect('/register')

    user = session.query(User).filter(User.email == user_email).first()

    if user:
        notes = session.query(Note).filter(Note.user == user).all()
        return render_template('mainpage.html', notes=notes, email=user_email)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_email
    error_messages = {'email': '', 'password': ''}

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email:
            error_messages['email'] = 'Please enter your email address.'
        elif not is_valid_email(email):
            error_messages['email'] = 'Invalid email address.'

        if not password:
            error_messages['password'] = 'Please enter your password.'
        elif not is_valid_password(password):
            error_messages['password_requirements'] = 'Password must be at least 8 characters long, contain at least one uppercase letter and at least one digit.'

        if not all(error == '' for error in error_messages.values()):
            return render_template('login.html', error_messages=error_messages)

        if check_email(email):
            if check_login(email, password):
                user_email = email
                return redirect('/')
            else:
                error_messages['password'] = 'Invalid password or email'
                return render_template('login.html', error_messages=error_messages)
        else:
            error_messages['password'] = 'Invalid password or email'
            return render_template('login.html', error_messages=error_messages)
    return render_template('login.html', error_messages={})

@app.route('/register', methods=['GET', 'POST'])
def registration():
    global user_email
    error_messages = {'email': '', 'password': ''}
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email:
            error_messages['email'] = 'Please enter your email address.'
        elif not is_valid_email(email):
            error_messages['email'] = 'Invalid email address.'
        if not password:
            error_messages['password'] = 'Please enter your password.'
        elif not is_valid_password(password):
            error_messages['password_requirements'] = 'Password must be at least 8 characters long, contain at least one uppercase letter and at least one digit.'

        if not all(error == '' for error in error_messages.values()):
            return render_template('register.html', error_messages=error_messages)

        if not check_email(email):
            user = User(email=email,password=hash_password(password).decode())
            session.add(user)
            session.commit()
            user_email = email
            return redirect('/')
        else:
            error_messages['password'] = 'Invalid password or email'
            return render_template('register.html', error_messages=error_messages)
    return render_template('register.html', error_messages={})

@app.route('/logout')
def logout():
    global user_email
    user_email = None
    return redirect('/register')

@app.route('/add_note', methods=['POST'])
def add_note():
    global user_email
    if user_email is None:
        return redirect('/register')

    user = session.query(User).filter_by(email=user_email).first()

    if user:
        title = request.form['title']
        text = request.form['text']
        new_note = Note(title=title, text=text, user=user)
        session.add(new_note)
        session.commit()
        return redirect(url_for('main'))
    return redirect('/register')

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    global user_email
    if user_email is None:
        return redirect('/register')

    user = session.query(User).filter_by(email=user_email).first()

    if user:
        note = session.query(Note).filter_by(id=note_id, user_id=user.id).first()
        if note:
            session.delete(note)
            session.commit()
            return redirect(url_for('main'))
    return redirect('/register')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    global user_email
    if user_email is None:
        return redirect('/register')

    user = session.query(User).filter_by(email=user_email).first()
    note = session.query(Note).filter_by(id=note_id, user_id=user.id).first()

    if request.method == 'POST':
        if note:
            note.title = request.form['title']
            note.text = request.form['text']
            session.commit()
            return redirect(url_for('main'))
    else:
        if note:
            return render_template('edit_note.html', note=note)
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.secret_key = 'tcccccc'