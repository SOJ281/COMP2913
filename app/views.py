from flask import Flask, request, redirect, url_for, render_template, flash

from .forms import LoginForm, SignupForm, BookingForm,ScooterForm
from app import app, models, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

@app.route('/first_item', methods=['GET', 'POST'])
def first():
    return render_template("first_item.html")

@app.route('/second_item', methods=['GET', 'POST'])
def second():
    return render_template("second_item.html")

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template("success.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = models.Users.query.filter_by(email=email).first()
        #check if the user exists and if the password is correct
        if not user or not check_password_hash(user.password, password):
            flash('Login details incorrect. Try again!')
            return render_template("login.html", form=form)
        login_user(user)
        if user.staff==True:
            return redirect(url_for('staff'))
        else:
            return redirect(url_for('booking'))
    return render_template("login.html", form=form)


@app.route("/staff", methods=['GET', 'POST'])
def staff():
    scooters = []
    for i in models.Scooters.query.all():
        scooters.append(i)
    return render_template("staff.html",Scooters = scooters)

@app.route("/add_scooter", methods=['GET', 'POST'])
def add_scooter():
    form = ScooterForm()
    if form.validate_on_submit():
        available = request.form.get('available')
        location = request.form.get('location')
       
        new_scooter = models.Scooters(available = available, location = location)
        
        db.session.add(new_scooter)
        db.session.commit()
        
        return redirect(url_for("staff"))
        
    return render_template("add_scooter.html",form = form)

@app.route("/config_scooter/<id>", methods=['GET', 'POST'])
def config_scooter(id):
    scooter = models.Scooters.query.get(id)
    form = ScooterForm()
    if form.validate_on_submit():
        s = scooter
        s.available = form.available.data
        s.location = form.location.data
        db.session.commit()
        return redirect('/staff')
    return render_template("config_scooter.html",form = form,scooter = scooter)


@app.route("/booking", methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        duration = request.form.get('duration')
        location = request.form.get('location')

        scooter = models.Scooters.query.filter_by(location=location, available=1).first()
        price = models.Prices.query.filter_by(duration=duration).first()

        #check if scooter at the location is free
        if scooter is None:
            flash('No scooter available at location!')
            return render_template("booking.html", form=form)

        #check if card payment successfully
        #changes after implementing card payments
        paid_successfully = False
        if not paid_successfully:
            flash('Payment Unsuccessful!')
            return render_template("booking.html", form=form)

        new_booking = models.Book(user_id=current_user.id, scooter_id=scooter.id, price_id=price.id)
        scooter.available = 2
        db.session.add(new_booking)
        db.session.commit()
        flash('Scooter booked successfully!')
    return render_template("booking.html", form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    # get and check input signup information form, if true then signup successfully
    if form.validate_on_submit():
        username = request.form.get('username')
        age = request.form.get('age')
        email = request.form.get('email')
        password = request.form.get('password')
        pw_confirm = request.form.get('pw_confirm')
        if not password == pw_confirm:
            flash("Passwords don't match. Try again!")
            # for now the whole form will be reload if passwords don't match
            #later try to reset only password fields
            render_template("signup.html", form=form)
        user = models.Users.query.filter_by(email=email).first() # checking if email address already in database
        userN = models.Users.query.filter_by(username=username).first() # checking of the username is taken
        if user:
            flash("An account with this email address already exists!")
            return render_template("signup.html", form=form)
        if userN:
            flash("This username is already taken!")
            return render_template("signup.html", form=form)
        new_user = models.Users(username=username, age=age, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))


@app.route('/price_view', methods=['GET', 'POST'])
def price_view():
    time_now = datetime.now()
    date_one = models.Book.query.filter(models.Book.datetime >= time_now - timedelta(days=7)).all()
    income_one = 0
    income_two = 0
    income_three = 0
    for i in date_one:
        print(i.price_id, i.datetime,)
        print(i.prices.duration, i.prices.cost)
        income_one += (i.prices.duration * i.prices.cost)
    print(income_one)
    date_two = models.Book.query.filter(models.Book.datetime >= time_now - timedelta(days=30)).all()
    for i in date_two:
        print(i.price_id, i.datetime,)
        print(i.prices.duration, i.prices.cost)
        income_two += (i.prices.duration * i.prices.cost)
    print(income_two)
    date_three = models.Book.query.filter(models.Book.datetime >= time_now - timedelta(days=1)).all()
    for i in date_three:
        print(i.price_id, i.datetime, )
        print(i.prices.duration, i.prices.cost)
        income_three += (i.prices.duration * i.prices.cost)
    print(income_three)
    if request.method == 'GET':
        return render_template("income.html", income_one=income_one, income_two=income_two, income_three=income_three)
