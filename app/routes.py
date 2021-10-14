from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, UserForm 
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        name = register_form.name.data
        phone = register_form.phone.data
        password = register_form.password.data
        print("submitted correctly")
        existing_user = User.query.filter_by(username=username).all()
        # if existing_user:
        #     flash(f'The username {username} is already in use. Please try again.', 'danger')
        #     return redirect(url_for('register'))
       
        new_user = User(username, email, name, phone, password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username}, you have successfully registered!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=register_form)

@app.route('/login', methods =['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('wrong username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Welcome {user.username}, you have successfully logged in.', 'success')

    return render_template('login.html', login_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
