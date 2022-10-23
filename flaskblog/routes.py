from flask import Flask, render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [
    {
        'author': 'nikita',
        'title': 'hey there',
        'content': 'first time',
        'date_posted': 'april 20, 2002'
    },
    {
        'author': 'matt',
        'title': 'hey there then',
        'content': 'first love time',
        'date_posted': 'april 3, 2002'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abc@gmail.com' and form.password.data == 'abc':
            flash('you have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('login unsuccessfully, please check user name and password', 'danger')
    return render_template('login.html', title='Login', form=form)
