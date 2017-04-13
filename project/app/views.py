# -*- coding:utf-8 -*-
import datetime
import sys
#from string import strip

from flask import (
    render_template, flash, redirect, session, url_for, request, g)
from flask_login import (
    login_user, logout_user, current_user, login_required)
from .forms import (
    LoginForm, SignUpForm, PublishBlogForm, AboutMeForm, PublishMovieForm)
from .models import ( Person )
from .utils import PER_PAGE

from app import app, db, lm

@lm.user_loader
def load_user(user_id):
    #return User.query.get(int(user_id))
    return Account.query.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    movies = Movie.query.order_by(
        db.desc(Movie.id)
    )
    return render_template(
        "index.html",
        title="Home",
        movies=movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_name'))

        if user:
            login_user(user)
            user.last_seen = datetime.datetime.now()

            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/login')

            flash('Your name: ' + request.form.get('user_name'))
            flash('remember me? ' + str(request.form.get('remember_me')))
            return redirect(url_for("users", user_id=current_user.id))
        else:
            flash('Login failed, Your name is not exist!')
            return redirect('/login')

    return render_template(
        "login.html",
        title="Sign In",
        form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        user_type = request.form.get('account_type')

        register_check = User.query.filter(db.or_(
            User.customer_id == user_name, User.email == user_email)).first()
        if register_check:
            flash("error: The user's name or email already exists!")
            return redirect('/sign-up')

        if len(user_name) and len(user_email):
            user.customer_id = user_name
            user.email = user_email
            user.type = user_type
            user.creation_data = datetime.datetime.now()
            '''
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/sign-up')
            '''

            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("Database error!")
                return redirect('/sign-up')

            flash("Sign up successful!")
            return redirect('/index')

    return render_template(
        "sign_up.html",
        form=form)


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id = None):
    form = SignUpForm()
    form.submit.type = 'SAVE'
    user = User.query.filter_by(
        id = current_user.id
        ).first()

    if form.validate_on_submit():
        user_name = request.form.get('user_name').strip()
        user_email = request.form.get('user_email').strip()
        user_type = request.form.get('account_type')

        last_name = request.form.get('last_name').strip()
        first_name= request.form.get('first_name').strip()
        address = request.form.get('address').strip()
        city = request.form.get('city').strip().upper()
        state = request.form.get('state').strip().upper()
        zipcode = request.form.get('zipcode').strip()
        phone = request.form.get('phone').strip()


        register_check = User.query.filter(db.and_(
            User.id != user.id, User.customer_id == user_name)).first()

        if register_check:
            flash("error: The user's name or email already exists!")
            return redirect(url_for("profile", user_id=user_id))

        if len(user_name) and len(user_email):
            user.customer_id = user_name
            user.email = user_email
            user.type = user_type

            user.last_name = last_name if len(last_name) else None
            user.first_name = first_name if len(first_name) else None
            user.address = address if len(address) else None
            user.city = city if len(city) else None
            user.state = state if len(state) else None
            user.zipcode = zipcode if len(zipcode) else None
            user.phone = phone if len(phone) else None

            '''
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/sign-up')
            '''

            try:
                db.session.add(user)
                db.session.commit()
            except:
                print('db err')
                flash("Database error!")
                return redirect(url_for("profile", user_id=user_id))
            print('return pro')
            flash("Sign up successful!")
            return redirect(url_for("profile", user_id=user_id))

    else:
        form.user_name.data = user.customer_id
        form.user_email.data = user.email
        form.account_type.data = user.type.name
        form.last_name.data = user.last_name
        form.first_name.data = user.first_name
        form.address.data = user.address
        form.city.data = user.city
        form.state.data = user.state
        form.zipcode.data = user.zipcode
        form.phone.data = user.phone
        return render_template(
            "profile.html",
            user_id=user_id,
            form=form)

@app.route('/user/<int:user_id>', defaults={'page':1}, methods=["POST", "GET"])
@app.route('/user/<int:user_id>/page/<int:page>', methods=['GET', 'POST'])
@login_required
def users(user_id, page):
    form = AboutMeForm()
    if user_id != current_user.id:
        flash("Sorry, you can only view your profile!", "error")
        return redirect("/index")

    # pagination = user.posts.paginate(page, PER_PAGE, False).items
    pagination = Post.query.filter_by(
        user_id = current_user.id
        ).order_by(
        db.desc(Post.timestamp)
        ).paginate(page, PER_PAGE, False)
    return render_template(
        "user.html",
        form=form,
        pagination=pagination)


@app.route('/publish/<int:user_id>', methods=["POST", "GET"])
@login_required
def publish(user_id):
    form = PublishBlogForm()
    posts = Post()
    if form.validate_on_submit():
        blog_body = request.form.get("body")
        if not len(blog_body.strip(" ")):
            flash("The content is necessray!")
            return redirect(url_for("publish", user_id=user_id))
        posts.body = blog_body
        posts.timestamp = datetime.datetime.now()
        posts.user_id = user_id

        try:
            db.session.add(posts)
            db.session.commit()
        except:
            flash("Database error!")
            return redirect(url_for("publish", user_id=user_id))

        flash("Publish Successful!", "success")
        return redirect(url_for("publish", user_id=user_id))

    return render_template(
        "publish.html",
        user_id=user_id,
        form=form)

@app.route('/publish_movie/<int:user_id>', methods=["POST", "GET"])
@login_required
def publish_movie(user_id):
    form = PublishMovieForm()
    movie = Movie()
    if form.validate_on_submit():
        name = request.form.get("name")
        copies = request.form.get("copies")
        fee = request.form.get("fee")
        movie_type = request.form.get('movie_type')
        actor1 = request.form.get("actor1")
        actor2 = request.form.get("actor2")
        actor3 = request.form.get("actor3")

        if not len(name.strip(" ")):
            flash("The content is necessray!")
            return redirect(url_for("publish_movie", user_id=user_id))

        movie.movie_name = name
        movie.type = movie_type
        movie.copies = copies
        movie.fee = fee

        try:
            db.session.add(movie)
            db.session.commit()
        except:
            flash("Database error!")
            return redirect(url_for("publish_movie", user_id=user_id))

        flash("Publish Successful!", "success")
        return redirect(url_for("publish_movie", user_id=user_id))

    return render_template(
        "publish_movie.html",
        form=form)


@app.route('/user/about-me/<int:user_id>', methods=["POST", "GET"])
@login_required
def about_me(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.method == "POST":
        content = request.form.get("describe")
        if len(content) and len(content) <= 140:
            user.about_me = content
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("Database error!")
                return redirect(url_for("users", user_id=user_id))
        else:
            flash("Sorry, May be your data have some error.")
    return redirect(url_for("users", user_id=user_id))

@app.route('/add/<int:user_id>/<int:movie_id>', methods=["POST", "GET"])
@login_required
def add(user_id, movie_id):
    user = User.query.filter(User.id == user_id).first()
    movie = Movie.query.filter(Movie.id == movie_id).first()
    print(user.cart.__len__())
    user.cart.append(movie)

    db.session.add(user)
    db.session.commit()

    flash("is added to Cart")
    return redirect(url_for('index'))
