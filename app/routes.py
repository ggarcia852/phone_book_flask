# from re import U
from app import app
from flask import render_template
from app.forms import UserForm
from app.models import User
from app import db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserForm()
    if register_form.validate_on_submit():
        print("You have registered correctly")
        name = register_form.name.data
        email = register_form.email.data
        phone = register_form.phone.data
        password = register_form.password.data
        print(name, email, phone, password)
        new_user = User(name, email, phone, password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html', form=register_form)
