from flask import Flask, request, redirect, url_for, render_template, flash
from .forms import LoginForm, SignupForm, BookingForm
from app import app, models, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


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
    return render_template("staff.html")


@app.route("/booking", methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        duration = request.form.get('duration')
        location = request.form.get('location')

        scooter = models.Scooters.query.filter_by(location=location, available=0).first()
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
        scooter.available = 1
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
        if user:
            flash("An account with this email address already exists!")
            return render_template("signup.html", form=form)
        new_user = models.Users(username=username, age=age, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route('/income', methods=['GET', 'POST'])
def priceview():
    time_now = datetime.now()
    date = Book.query.filter(Book.datetime >= time_now - timedelta(days=7)).all()
    income = 0
    for i in date:
        print(i.price_id, i.datetime,)
        print(i.prices.duration, i.prices.cost)
        income += (i.prices.duration * i.prices.cost)
    print(income)
    return str(income)
