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

tests = {
    "cancer": ["Blood tests - CBC", "tumor marker Imaging tests  -CT Scan", "MRI"],
    "alzheimer's disease": ["brain imaging tests -MRI", "CT", "PET"],
    "arthritis": ["Blood tests - ESR", "CRP"],
    "dementia": ["Cognitive and neurological tests", "Brain scan"],
    "diabetes": ["A1C Test"],
    "heart disease": ["ECG", "cardiac CT scan", "cardiac MRI"],
    "high blood pressure": ["Ambulatory monitoring blood", "urine tests", "ECG"],
    "multiple sclerosis": ["MRI Scan"],
    "parkinson's disease": ["SPECT Scan", "DAT scan"],
    "spina bifida": ["MSAFP Test"],
    "thyroid disorders": ["TSH", "T3-T4", "TSI", "antithyroid antibody test"]
}

symptoms = {
    "cancer": ["weight loss", "fatigue", "fever", "skin changes"],
    "alzheimer's disease": ["forgetting recent events", "misplacing items", "asking questions repetetively"],
    "arthritis": ["fatigue", "fever", "loss of apetite", "swollen joints", "joint stiffness"],
    "dementia": ["memory loss", "difficulty in concentrating", "confusion", "mood changes"],
    "diabetes": ["very thirsty", "very hungry", "weight loss", "urinate alot"],
    "heart disease": ["chest pain", "shortness of breath", "pain in the neck", "jaw and back"],
    "high blood pressure": ["dizziness", "nervousness", "sweating", "trouble sleeping"],
    "multiple sclerosis": ["loss of vision", "loss of power in arm", "numbness in leg"],
    "parkinson's disease": ["tremor", "slowed movement", "rigid muscles", "impaired posture"],
    "spina bifida": ["weakness or total paralysis of legs", "bowel incontinence", "loss of skin sensation in legs"],
    "thyroid disorders": ["fatigue", "constipation", "dry skin", "weight gain"]
}



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


category_d = ["Fine", "Mild", "Moderate", "Severe", "Intense"]


@app.route("/prediction", methods=['GET', 'POST'])
@login_required
def prediction():
    form = PredictForm()
    if form.validate_on_submit():
        dis = form.disease.data
        mom = form.mom.data
        mom = float(int(mom)/100)
        dad = form.dad.data
        dad = float(int(dad) / 100)
        arr = np.array([mom, dad])
        p = round(model.predict([arr])[0], 2)
        test = []
        sysm = []
        #specialist = []
        disease_catr = ""
        #nikitha_test(predict, disease, test, sysm, disease_catr)
        if p < .17:
            test.append(tests[dis][0])
            sysm.append(symptoms[dis[0]])
            disease_catr = category_d[0]
        elif p < .34 and p > .18:
            test.append(tests[dis][0])
            sysm.append(symptoms[dis[0]])
            sysm.append(symptoms[dis[1]])
            disease_catr = category_d[1]
        elif p < .5 and p > .34:
            test.append(tests[dis][0])
            # test = test.append(tests[dis][-1])
            sysm = symptoms[dis]
            disease_catr = category_d[2]
        elif p < .67 and p > .51:
            test.append(tests[dis][0])
            # test = test.append(tests[dis][-1])
            sysm = symptoms[dis]
            disease_catr = category_d[3]
        else:
            test = tests[dis]
            sysm = symptoms[dis]
            disease_catr = category_d[4]

        print(test)
        print(sysm)
        print("hey")
        #flash('prob is  {}'.format(p))
        return render_template('predict_out.html', disease_catr=disease_catr, disease=dis, test=test, sysm=sysm)


    return render_template('prediction.html', title='New Post', form=form, legend='Predict')