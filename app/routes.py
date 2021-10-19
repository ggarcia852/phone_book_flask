from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, PhonebookForm, UserForm 
from app.models import Phonebook, User
from flask_login import login_user, logout_user, current_user, login_required



@app.route('/')
def index():
    title = "PhoneBook App"
    contacts = Phonebook.query.all()

    return render_template('index.html', contacts=contacts, title=title)



@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Register New User"
    register_form = UserForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        existing_user = User.query.filter_by(username=username).all()
        if existing_user:
            flash(f'The username {username} is already in use. Please try again.', 'danger')
            return redirect(url_for('register'))
       
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username}, you have successfully registered!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=register_form, title=title)



@app.route('/login', methods=['GET', 'POST'])
def login():
    title= 'Login'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()


        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'danger')
            return redirect(url_for('login'))

        login_user(user)

        flash(f'Welcome {user.username}. You have successfully logged in.', 'success')

        return redirect(url_for('index'))

    return render_template('login.html', title=title, login_form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    title = "Add New Contact"
    contact = PhonebookForm()
    if contact.validate_on_submit():
        first = contact.first_name.data
        last = contact.last_name.data
        phone = contact.phone.data
        email = contact.email.data
        address = contact.address.data

        new_contact = Phonebook(first, last, phone, email, address)
        db.session.add(new_contact)
        db.session.commit()

        flash('New Contact Added Successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add_contact.html', form=contact, title=title)

