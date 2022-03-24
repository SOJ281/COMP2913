from flask import Flask, request, redirect, url_for, render_template, flash
from .forms import LoginForm, SignupForm, BookingForm,ScooterForm,PriceForm,AddPriceForm,CardForm, monthInputForm
from app import app, models, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from .scooteremail import sendConfirmationMessage

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    bookings = []
    prices = []
    scooters = []
    for i in models.Book.query.all():
        if (i.user_id == current_user.id):
            bookings.append(i)
            prices.append(models.Prices.query.get(i.price_id))
            scooters.append(models.Scooters.query.get(i.scooter_id))
    return render_template("profile.html", name=current_user.username, Bookings=bookings, Prices=prices, Scooters=scooters)

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

@app.route("/add_price", methods=['GET', 'POST'])
def add_price():
    form = AddPriceForm()
    if form.validate_on_submit():
        duration = request.form.get('duration')
        cost = request.form.get('cost')
        new_price = models.Prices(duration = duration, cost = cost)
        db.session.add(new_price)
        db.session.commit()
        return redirect(url_for("price"))
    return render_template("add_price.html")

@app.route("/delete_price/<id>", methods=['GET', 'POST'])
def delete_price(id):
    price = models.Prices.query.get(id)
    db.session.delete(price)
    db.session.commit()
    return redirect('/price')

@app.route("/config_scooter/<id>", methods=['GET', 'POST'])
def config_scooter(id):
    s = models.Scooters.query.get(id)
    form = ScooterForm()
    if form.validate_on_submit():
        new_availability = form.available.data
        if s.available == 2 and new_availability == 1:
            booking = models.Book.query.filter_by(scooter_id=id).first()
            if booking is not None:
                booking.completed = 1
        s.available = new_availability
        s.location = form.location.data
        db.session.commit()
        return redirect('/staff')
    return render_template("config_scooter.html",form = form,scooter = s)

@app.route("/config_price/<id>", methods=['GET', 'POST'])
def config_price(id):
    price = models.Prices.query.get(id)
    form = PriceForm()

    if form.validate_on_submit():
        p = price
        p.cost = form.cost.data
        db.session.commit()
        return redirect('/price')
    return render_template("config_price.html",form = form, price = price)


@app.route("/booking", methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        duration = int(request.form.get('duration'))
        location = request.form.get('location')

        scooter = models.Scooters.query.filter_by(location=location, available=1).first()
        price = models.Prices.query.filter_by(duration=duration).first()
        curdatetime = datetime.now()

        #check if scooter at the location is free
        if scooter is None:
            flash('No scooter available at location!')
            return render_template("booking.html", form=form)

        new_booking = models.Book(user_id=current_user.id, scooter_id=scooter.id, price_id=price.id, datetime=curdatetime, completed=0)
        scooter.available = 2
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('card'))
    return render_template("booking.html", form=form)

@app.route('/card', methods=['GET', 'POST'])
@login_required
def card():
    form = CardForm()
    if form.validate_on_submit():
        number_string = request.form.get('number')
        expiration_date_string = request.form.get('expiration_date')
        security_code = int(request.form.get('security_code'))
        name = request.form.get('name')

        curdatetime = datetime.now()
        success = True

        # Validate card number
        try:
            if len(number_string) != 16:
                raise ValueError
            number = int(number_string)
        except ValueError:
            success = False

        # Validate expiration date
        try:
            parts = expiration_date_string.split("/")
            if len(parts) != 2:
                raise ValueError
            month = int(parts[0])
            year = int(parts[1])
            if month not in range(1, 13) or year not in range(22, 100):
                raise ValueError
            if year == (curdatetime.year % 1000) and month < curdatetime.month:
                raise ValueError
        except ValueError:
            success = False

        # Validate security code
        if security_code not in range(100, 1000):
            success = False

        new_booking = models.Book.query.filter_by(user_id=current_user.id).order_by(models.Book.id.desc()).first()
        scooter = new_booking.scooters
        price = new_booking.prices

        if not success:
            db.session.delete(new_booking)
            scooter.available = 1
            db.session.commit()
            flash("Payment Unsuccesful, plase check card details")
            return redirect(url_for('booking'))

        durations = {1: "1 hour",
                     4: "4 hours",
                     24: "1 day",
                     168: "1 week"}

        sendConfirmationMessage(current_user.username, current_user.email, scooter.id, scooter.location, (str(curdatetime.hour)+":"+str(curdatetime.minute)), curdatetime.date(), durations.get(price.duration))
        flash('Scooter booked successfully! Please check your email for the Booking Confirmation')
        return redirect(url_for("profile"))
    return render_template("card.html",form=form)

@app.route("/cancel_booking/<id>", methods=['GET', 'POST'])
def cancel_booking(id):
    time = datetime.now()
    booking = models.Book.query.get(id)

    diff = time - booking.datetime
    if diff.seconds < 900:
        scooter = booking.scooters
        scooter.available = 1
        db.session.delete(booking)
        db.session.commit()
        flash("Booking cancelled successfully")
    else:
        flash("Failed to cancel booking. You can only cancel within 15 minutes of booking")
    return redirect('/profile')

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
    form = monthInputForm()
    time_now = datetime.now()

    total_income = 0
    final_date = ""

    income_Ar = []
    income_DateAr = []

    #Determines graph data and returns for days and total
    if form.validate_on_submit():
        viewType = request.form.get('viewType')
        day = int(request.form.get('day'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))

        if (viewType == "Weekly"): #If weekly view
            myDate = datetime(year, month, day)
            final_date = "Week of "+myDate.strftime("%x")
            while(not myDate.strftime("%w") == "0"):
                myDate = myDate - timedelta(days=1)
            for l in range(0, 7):
                myDate = myDate + timedelta(days=1)
                date_results = models.Book.query.filter((models.Book.datetime <= myDate) & (models.Book.datetime >=  myDate - timedelta(days=1))).all()
                temp_val = 0
                for i in date_results:
                    temp_val = (i.prices.duration * i.prices.cost)
                    total_income += temp_val
                import calendar
                income_DateAr.append(l+1)
                income_Ar.append(temp_val)

        if (viewType == "Monthly"): #If monthly view
            from calendar import monthrange
            length = monthrange(2019, 2)[1]
            final_date = "Month of "+datetime(year, month, 1).strftime("%d") + "/" + datetime(year, month, 1).strftime("%Y")
            for l in reversed(range(1, length)):
                myDate = datetime(year, month, length - l)
                date_results = models.Book.query.filter((models.Book.datetime <= myDate) & (models.Book.datetime >=  myDate - timedelta(days=1))).all()
                temp_val = 0
                for i in date_results:
                    temp_val = (i.prices.duration * i.prices.cost)
                    total_income += (i.prices.duration * i.prices.cost)
                income_DateAr.append(length - l)
                income_Ar.append(temp_val)

        if (viewType == "Yearly"): #If Yearly view
            myDatec = datetime(year-1, 12,  1)
            final_date = "Year of "+ datetime(year, month, 1).strftime("%Y")
            for l in range(1, 13):
                myDate = datetime(year, l,  1)
                date_results = models.Book.query.filter((models.Book.datetime <= myDate) & (models.Book.datetime >= myDatec)).all()
                temp_val = 0
                for i in date_results:
                    temp_val = (i.prices.duration * i.prices.cost)
                    total_income += (i.prices.duration * i.prices.cost)
                income_DateAr.append(l)
                income_Ar.append(temp_val)
                myDatec = datetime(year, l,  1)


    return render_template("income.html", final_date=final_date, total_income=total_income, income_Ar=income_Ar, income_DateAr=income_DateAr, form=form)


@app.route("/price", methods=['GET', 'POST'])
def price():
    prices = []
    for i in models.Prices.query.all():
        prices.append(i)
    return render_template("price.html",Prices = prices)
