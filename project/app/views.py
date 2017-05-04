# -*- coding:utf-8 -*-
import datetime
import sys
#from string import strip
from flask import (
    render_template, flash, redirect, session, url_for, request, g)
from flask_login import (
    login_user, logout_user, current_user, login_required)
from .forms import *
from .models import *
from .utils import *
from app import app, db, lm

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

@lm.user_loader
def load_user(user_id):
    #return User.query.get(int(user_id))
    return Accounts.query.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        movies = getMovies(18, current_user.Id)
    else:
        movies = getMovies(18)
    hotMovies = getHotMovies()
    res = getHotReviews()
    types = get10MovieType()
    return render_template(
        "index.html",
        title="Home",
        movies=movies,
        hotMovies=hotMovies,
        res=res,
        types=types)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        user = Accounts.login_check(request.form.get('user_email'),
                                request.form.get('user_password'))

        if user:
            login_user(user)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                traceback.print_exc(file=sys.stdout)
                session.rollback()
                return redirect('/sign_in')

            if current_user.UserName:
                flash('Welcome back: ' + current_user.UserName)
            else:
                flash('Welcome back: ' + current_user.Email)
            return redirect('/')
        else:
            flash('Login failed, Your name is not exist!')
            return redirect('/sign_in')

    return render_template(
        "sign_in.html",
        title="Sign In",
        form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    print('sign up ing')
    form = SignUpForm()
    account = Accounts()
    session = db.session()
    if form.validate_on_submit():
        account.UserName = request.form.get('user_name')
        account.PassWord = request.form.get('user_password')
        account.Type = request.form.get('account_type')
        account.Email = request.form.get('user_email')
        account.CreditCardNumber = request.form.get('credit_card')
        account.LastName = request.form.get('last_name')
        account.FirstName = request.form.get('first_name')
        account.Address = request.form.get('address')
        account.ZipCode = request.form.get('zipcode')
        account.Phone = None if not request.form.get('phone') else request.form.get('phone')
        register_check = Accounts.login_check(account.UserName, account.PassWord)
        if register_check:
            flash("error: The user's name or email already exists!")
            return redirect('/')
        zipcode_check = session.query(Location).filter_by(ZipCode=account.ZipCode).first()
        if not zipcode_check:
            newLocation = Location()
            newLocation.ZipCode = account.ZipCode
            newLocation.City = request.form.get('city')
            newLocation.State = request.form.get('state')
            session.add(newLocation)
            session.commit()
        try:
            session.add(account)
            session.commit()
        except:
            flash("Database error!")
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            return redirect('/')
        login_user(account)
        flash("Sign up successful!")
        return redirect('/')

    return render_template(
        "profile.html",
        title='PROFILE',
        action=0,   #sign up
        form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('search_text')
    if query:
        movies, actors = dataSearch(query)
        return render_template(
            "list.html",
            title='SEARCH',
            movies=movies,
            actors=actors,
            action=5)
    return redirect('/')

@app.route('/review/<int:review_id>', methods=['GET', 'POST'])
def review(review_id):
    rev = getReviewById(review_id)
    if not rev:
        return redirect('/')
    movie = getMovieById(rev.MovieId)
    if movie:
        return render_template(
            "review.html",
            title='Revie Of ' + movie.Name,
            movie=movie,
            rev=rev)
    return redirect('/')

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie(movie_id = None):
    movie = getMovieById(movie_id)
    actors = getActors(movie_id)
    if current_user.is_authenticated:
        movies = getMovies(12, current_user.Id)
    else:
        movies = getMovies(12)
    res = getReviews(movie_id)
    rateform = PublishBlogForm()
    return render_template(
        "movie.html",
        title=movie.Name,
        movie=movie,
        movies=movies,
        actors=actors,
        form=rateform,
        res=res)

@app.route('/actor/<int:actor_id>', methods=['GET', 'POST'])
def actor(actor_id = None):
    actor = getActor(actor_id)
    movies = getMoviesByActorId(actor_id)
    return render_template(
        "actor.html",
        title=actor.Name,
        movies=movies,
        actor=actor)

@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id = None):
    form = SignUpForm()
    form.submit.data = 'SAVE'
    session = db.session()
    if not user_id and current_user.is_authenticated():
        user_id = current_user.get_id()
        account = current_user
    else:
        account = getAccount(user_id)

    if account.ZipCode:
        location = session.query(Location).filter_by(ZipCode=account.ZipCode).first()
    else:
        location = Location()

    #account = getAccount(user_id)
    #account = session.query(Accounts).filter_by(Id=user_id).first()
    if form.validate_on_submit():
        account = session.query(Accounts).filter_by(Id=user_id).first()
        account.Customer = request.form.get('user_ssn')
        account.UserName = request.form.get('user_name')
        account.PassWord = request.form.get('user_password')
        account.Email = request.form.get('user_email')
        account.CreditCardNumber = request.form.get('credit_card')
        account.LastName = request.form.get('last_name')
        account.FirstName = request.form.get('first_name')
        account.Address = request.form.get('address')
        account.ZipCode = None if not request.form.get('zipcode') \
                            else int(request.form.get('zipcode'))
        account.Phone = None if not request.form.get('phone') \
                             else int(request.form.get('phone'))
        upType = 0
        if account.is_admin():
            form.account_type.data = account.Type
        else:
            upType = 1 if request.form.get('account_type') > account.Type else 0
            account.Type = request.form.get('account_type')

        zipcode_check = session.query(Location).filter_by(ZipCode=account.ZipCode).first()
        if not zipcode_check:
            newLocation = Location()
            newLocation.ZipCode = account.ZipCode
            newLocation.City = request.form.get('city')
            newLocation.State = request.form.get('state')
            session.add(newLocation)
            session.commit()
        else:
            zipcode_check.City = request.form.get('city');
            zipcode_check.State = request.form.get('state');

        try:
            session.commit()
        except:
            flash("Database error!")
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            render_template(
                "profile.html",
                action=1,
                form=form)
        print('return pro')
        if upType:
            flash("Thanks for Your $$$!")
        else:
            flash("Saved successful!")
        return render_template(
            "profile.html",
            title="PROFILE",
            action=1,   #profile
            form=form)

    form.user_name.data = account.UserName
    form.user_password.data = account.PassWord
    form.account_type.data = account.Type
    form.last_name.data = account.LastName
    form.first_name.data = account.FirstName
    form.address.data = account.Address
    form.zipcode.data = account.ZipCode
    form.phone.data = account.Phone
    form.credit_card.data = account.CreditCardNumber
    form.user_email.data = account.Email

    if account.ZipCode:
        localtion = session.query(Location).filter_by(ZipCode=account.ZipCode).first()
        form.city.data = location.City
        form.state.data = location.State
    return render_template(
        "profile.html",
        form=form)

@app.route('/user/<int:user_id>', defaults={'page':1}, methods=["POST", "GET"])
@app.route('/user/<int:user_id>/page/<int:page>', methods=['GET', 'POST'])
@login_required
def users(user_id, page):
    form = AboutMeForm()
    if user_id != current_user.Id:
        flash("Sorry, you can only view your profile!", "error")
        return redirect("/")

    # pagination = user.posts.paginate(page, PER_PAGE, False).items
    return render_template(
        "user.html",
        form=form)


@app.route('/publish/<int:movie_id>', methods=["POST", "GET"])
@login_required
def publish(movie_id):
    form = PublishBlogForm()
    review = Reviews()
    session = db.session()
    if form.validate_on_submit():
        blog_body = request.form.get("body")
        movie = getMovieById(movie_id)
        if not len(blog_body.strip(" ")):
            flash("The content is necessray!")
            return redirect(url_for("movie", movie_id=movie_id))
        review.Content = blog_body
        review.Author = current_user.UserName if current_user.UserName else current_user.Email[:5] + '****'
        review.MovieId = movie_id
        review.AccountId = current_user.Id
        rate = int(request.form.get("rate"))
        if rate == 1:
            movie.Num1Rating += 1
        elif rate == 2:
            movie.Num2Rating += 1
        elif rate == 3:
            movie.Num3Rating += 1
        elif rate == 4:
            movie.Num4Rating += 1
        elif rate == 5:
            movie.Num5Rating += 1

        try:
            session.add(review)
            session.commit()
        except:
            flash("Database error!")
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            return redirect(url_for("movie", movie_id=movie_id))

        flash("Publish Successful!", "success")
        return redirect(url_for("movie", movie_id=movie_id))

    return redirect( "/")

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

@app.route('/list')
@app.route('/list/<int:action>/<int:page>', methods=["POST", "GET"])
@app.route('/list/<int:action>/<string:query>', methods=["POST", "GET"])
@app.route('/list/<int:action>/<string:query>/<int:page>', methods=["POST", "GET"])
def list(action, query = None, page = None, type = None):
    print("get ", action, query)
    session = db.session()
    if current_user.is_authenticated:
        user_id = current_user.get_id()

        if action == 1: # view Order List
            orders, movies = getOrders(user_id, 0)
            fOrders, fMovies = getOrders(user_id, 1)
            if not orders and not fOrders:
                flash("Empty Order List")
            return render_template(
                "list.html",
                orders=orders,
                movies=movies,
                fOrders=fOrders,
                fMovies=fMovies,
                page=None,
                action=action)
        elif action == 2: # view MovieQ List
            print('get action, ', action)
            movies = getMovieQ(user_id)
            print('find movies:', movies)
            if not movies:
                flash("Empty Queue")
            return render_template(
                "list.html",
                movies=movies,
                action=action)
        elif action == 3: # view MovieF List
            movies = getMovieF(user_id)
            if not movies:
                flash("Empty F")
            return render_template(
                "list.html",
                movies=movies,
                action=action)
        elif action == 4: # view reivew list
            pass

    if action == 5: # search list, not require log in
        movies, reviews, actors, locations = search(query)
        return render_template(
            "list.html",
            title='Search',
            movies=movies,
            reviews=reviews,
            actors=actors,
            locations=locations,
            action=action)
    elif action == 6: # list all
        num = 20
        movies = getMovies(page * num)[(num * (page-1)) : (page * num)]
        return render_template(
            "list.html",
            movies=movies,
            action=action,
            page=page)
    elif action == 7: # list by type
        num = 20
        movies = getMovieByType(query, page * num)[(num * (page-1)) : (page * num)]
        return render_template(
            "list.html",
            title=query,
            movies=movies,
            action=action,
            movie_type=query,
            page=page)
    return redirect_back('/')

@app.route('/add/<int:action>/<int:movie_id>', methods=["POST", "GET"])
def add(action, movie_id):
    session = db.session()
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        movie = getMovieById(movie_id)
        if action == 1: # add to OrderId, rent dvd
            res = addOrder(user_id, movie_id, movie.DistrFee)
            if res == 1:
                flash("is added to Order")
            elif res == 0:
                flash("db err")
            elif res == 2:
                flash("update ur account for more movie")
            elif res == 3:
                flash("u only can have " + str(current_user.get_limit()) + " at one time" )
            elif res == 4:
                flash("Its already in rented")
            redirect('/')
        elif action == 2: # add to MovieQ
            if addMovieQ(user_id, movie_id):
                flash(movie.Name + " is added to Queue")
                redirect('/')
            else:
                flash(movie.Name + " is NOT added to Queue")
                redirect('/')
        elif action == 3: # add to MovieF
            if addMovieF(user_id, movie_id):
                flash(movie.Name + " is added to F")
                redirect('/')
            else:
                flash(movie.Name + " NO added to F")
                redirect('/')
        elif action == 4: # add reivew
            pass
        elif action == 5: # return movie
            res = returnMovie(user_id, movie_id)
            if res == 1:
                flash("Thank you!")
                redirect('/')
            elif res == 0:
                flash("db err!")
                redirect('/')
            elif res == 2:
                flash("cant find this movie in list!")
                redirect('/')
        elif action == 6: # remove to MovieQ
            if removeMovieQ(user_id, movie_id):
                flash("removed to Queue")
                redirect('/')
            else:
                flash("NO added to Queue")
                redirect('/')
        elif action == 7: # remove to MovieF
            if removeMovieF(user_id, movie_id):
                flash("removed to F")
                redirect('/')
            else:
                flash("err to F")
                redirect('/')
    return redirect('sign_in')

@app.route('/admin/<int:action>/<int:i>', methods=["POST", "GET"])
def admin(action, i):
    session = db.session()
    if current_user.is_admin():
        if action == 1: #user list
            accounts = getUsers(i)
            return render_template(
                "admin.html",
                title='User List',
                accounts=accounts,
                action=action,
                page=i)
        elif action == 2:
            emps = getEmployees(i)
            return render_template(
                "admin.html",
                title='Emps List',
                emps=emps,
                action=action,
                page=i)
        elif action == 3: #order list
            orders = getOrdersList(i)
            return render_template(
                "admin.html",
                title='Order List',
                orders=orders,
                action=action,
                page=i)
        elif action == 4: #movie list
            movies = getMoviesList(i)
            return render_template(
                "admin.html",
                title='Movie List',
                movies=movies,
                action=action,
                page=i)
        elif action == 5: #actor list
            actors = getActorsList(i)
            return render_template(
                "admin.html",
                title='Order List',
                actors=actors,
                action=action,
                page=i)
    return redirect('/')


@app.route('/upgrade/<int:userId>/<int:i>', methods=["POST", "GET"])
def upgrade(userId, i): # i 0, cusmRep,  i 1 Admin
    if i == 0:
        upgradeToCustRep(userId)
    elif i == 1:
        upgradeToAdmin(userId)
    flash("Upgraded!")
    return redirect('/admin/1/1')

@app.route('/remove/<int:type>/<int:id>', methods=["POST", "GET"])
def remove(type, id): # type 0 acc, 1 movie, 2 actor
    if type == 0:
        delUser(id)
        flash("deleted!")
        return redirect('/admin/1/1')
    elif type == 1:
        delMovie(id)
        flash("deleted!")
        return redirect('/admin/4/1')
    elif type == 2:
        delActor(id)
        flash("deleted!")
        return redirect('/admin/5/1')
    flash("Error!")
    return redirect('/admin/1/1')


@app.route('/edit_movie', methods=['GET', 'POST'])
@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id = None):
    form = PublishMovieForm()
    session = db.session()
    if not current_user.is_authenticated() or not current_user.is_admin():
        return redirect('/')
    if movie_id:
        movie = session.query(Movie).filter_by(Id=movie_id).first()
    else:
        movie_id = None
        movie = Movie()
    if form.validate_on_submit():
        movie.Name = request.form.get('name')
        movie.Type = request.form.get('movie_type')
        movie.NumCopies = request.form.get('copies')
        movie.ImageUrl = request.form.get('posterUrl')
        movie.TrailerUrl = request.form.get('trailerUrl')
        movie.Language = request.form.get('language')
        movie.Length = request.form.get('length')
        movie.Director = request.form.get('director')
        movie.ReleaseDate = request.form.get('releaseDate')
        movie.ImdbId = request.form.get('imdbId')
        movie.Synopsis = request.form.get('synopsis')
        if not movie_id:
            session.add(movie)
        try:
            session.commit()
        except:
            flash("Database error!")
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            return redirect('/')
        print('return pro')
        flash(movie.Name + " is Added!")
        return redirect('/')
    form.name.data = movie.Name
    form.movie_type.data= movie.Type
    form.copies.data = movie.NumCopies
    form.posterUrl.data = movie.ImageUrl
    form.trailerUrl.data = movie.TrailerUrl
    form.language.data = movie.Language
    form.length.data = movie.Length
    form.director.data = movie.Director
    form.releaseDate.data = movie.ReleaseDate
    form.imdbId.data = movie.ImdbId
    form.synopsis.data = movie.Synopsis
    return render_template(
        "publish_movie.html",
        movie_id=movie_id,
        form=form)

@app.route('/edit_actor', methods=['GET', 'POST'])
@app.route('/edit_actor/<int:actor_id>', methods=['GET', 'POST'])
@login_required
def edit_actor(actor_id = None):
    form = ActorForm()
    session = db.session()
    if not current_user.is_authenticated() or not current_user.is_admin():
        return redirect('/')
    if actor_id:
        actor = session.query(Actor).filter_by(Id=actor_id).first()
    else:
        actor_id = None
        actor = Actor()
    if form.validate_on_submit():
        actor.Name = request.form.get('name')
        actor.Dob= request.form.get('dob')
        actor.Biography = request.form.get('biography')
        actor.ImdbId = request.form.get('imdbId')
        actor.BirthPlace = request.form.get('birthPlace')
        actor.ImageUrl = request.form.get('imageUrl')
        if not actor_id:
            session.add(actor)
        try:
            session.commit()
        except:
            flash("Database error!")
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            return redirect('/')
        print('return pro')
        if not actor_id:
            flash(actor.Name + " is Added!")
        else:
            flash(actor.Name + " is Saved!")
        return redirect('actor/'+str(actor.Id))
    form.name.data = actor.Name
    form.dob.data = actor.Dob
    form.biography.data = actor.Biography
    form.birthPlace.data = actor.BirthPlace
    form.imdbId.data = actor.ImdbId
    form.imageUrl.data = actor.ImageUrl
    return render_template(
        "publish_actor.html",
        title='ACTOR',
        actor_id=actor_id,
        form=form)

@app.route('/edit_emp', methods=['GET', 'POST'])
@app.route('/edit_emp/<int:emp_id>', methods=['GET', 'POST'])
@login_required
def edit_emp(emp_id = None):
    form = EmpForm()
    session = db.session()

    if not current_user.is_authenticated() or not current_user.is_admin():
        return redirect('/')

    if emp_id:
        emp = session.query(Employee).filter_by(Id=emp_id).first()
    else:
        emp_id = None
        emp = Employee()

    if form.validate_on_submit():
        emp.SSN = request.form.get('SSN')
        emp.StartDate = request.form.get('startDate')
        emp.HourlyRate= request.form.get('hourlyRate')
        emp.AccountId = request.form.get('accountId')
        if not emp_id:
            session.add(emp)
        try:
            session.commit()
        except:
            flash("Database error!")
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            return redirect('/')
        print('return pro')
        flash("Saved!")
        return redirect('edit_emp/'+str(emp.Id))
    form.SSN.data = emp.SSN
    form.startDate.data = emp.StartDate
    form.hourlyRate.data = emp.HourlyRate
    form.accountId.data = emp.AccountId
    return render_template(
        "edit_emp.html",
        title='Employee',
        emp_id=emp_id,
        form=form)
