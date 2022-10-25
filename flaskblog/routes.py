from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PredictForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets # for generating random picture file names so that they do not collide
import os # for knowing extension of the file
from PIL import Image # for resizing images automatically
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")

model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('login unsuccessfully, please check user name and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#if form.email.data == 'abc@gmail.com' and form.password.data == 'abc':
# flash('you have been logged in!', 'success')
# return redirect(url_for('home'))
#else:
#  flash('login unsuccessfully, please check user name and password', 'danger')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename

@app.route("/account",  methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)#can pass as many parameters as needed to rendering

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created', 'success') #here success is bootstrap class // documentation nk
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='new_post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='update_post', form=form, legend='update_post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('your post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/prediction", methods=['GET', 'POST'])
@login_required
def prediction():
    form = PredictForm()
    if form.validate_on_submit():
        #post = Post(mom=form.mom.data, dad=form.dad.data, author=current_user)
        #db.session.add(post)
        #db.session.commit()
        ans = form.mom.data
        ans = float(int(ans)/100)
        temo = form.dad.data
        temo = float(int(temo) / 100)
        #flash('prob is  {}'.format(temo))
        #flash('prob is  {}'.format(ans))
        arr = np.array([ans, temo])
        predict = model.predict([arr])[0]
        flash('prob is  {}'.format(predict))
       # return redirect(url_for('prediction'))
    return render_template('prediction.html', title='New Post', form=form, legend='Predict')