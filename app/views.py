from flask import Flask, request, redirect, url_for, render_template, flash
from .forms import LoginForm, SignupForm, BookingForm,ScooterForm,PriceForm,\
    AddPriceForm,CardForm, monthInputForm, feedbackForm, GuestForm
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
    duration = []
    scooters = []
    for i in models.Book.query.all():
        if (i.user_id == current_user.id):
            bookings.append(i)
            prices.append(i)
            scooters.append(models.Scooters.query.get(i.scooter_id))
    return render_template("profile.html", name=current_user.username, Bookings=bookings, Prices=prices, Scooters=scooters)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = feedbackForm()
    str1 = "not working"
    temp_comment = request.form.get('comments')
    if form.validate_on_submit():
        comment = request.form.get('comments')
        if str1 in temp_comment.lower():
            priority = 1
        else:
            priority = 2
        new_comment = models.Feedback(user_id=current_user.id, comments=comment, priority = priority)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template("feedback.html", form=form)

@app.route('/view_feedback', methods=['GET', 'POST'])
def view_feedback():
    users = []
    comments = []
    for i in models.Feedback.query.all():
        if i.priority == 1:
            comments.append(i)
            users.append(models.Users.query.get(i.user_id))
    for i in models.Feedback.query.all():
        if i.priority == 2:
            comments.append(i)
            users.append(models.Users.query.get(i.user_id))
    return render_template("view_feedback.html",Comments = comments, Users = users)

@app.route('/all_bookings', methods=['GET', 'POST'])
def all_bookings():
    bookings = []
    prices = []
    scooters = []
    users = []
    for i in models.Book.query.all():
        bookings.append(i)
        prices.append(i)
        scooters.append(models.Scooters.query.get(i.scooter_id))
        users.append(models.Users.query.get(i.user_id))
    return render_template("all_bookings.html", Users=users, Bookings=bookings, Prices=prices, Scooters=scooters)

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
        if user.staff==0:
            return redirect(url_for('booking'))
        elif user.staff==1:
            return redirect(url_for('employee'))
        elif user.staff==2:
            return redirect(url_for('staff'))
    return render_template("login.html", form=form)

@app.route("/staff", methods=['GET', 'POST'])
def staff():
    scooters = []
    for i in models.Scooters.query.all():
        scooters.append(i)
    return render_template("staff.html",Scooters = scooters)

@app.route("/employee", methods=['GET', 'POST'])
def employee():
    form = GuestForm()

    prices_dict = {}
    prices = models.Prices.query.all()
    for p in prices:
        prices_dict[p.duration] = p.cost

    if form.validate_on_submit():
        username = request.form.get('username')
        email = request.form.get('email')
        duration = int(request.form.get('duration'))
        location = request.form.get('location')

        scooter = models.Scooters.query.filter_by(location=location, available=1).first()
        price = models.Prices.query.filter_by(duration=duration).first()
        curdatetime = datetime.now()

        #check if scooter at the location is free
        if scooter is None:
            flash('No scooter available at location!')
            return render_template("employee.html", form=form, Prices=prices_dict)

        new_booking = models.Book(user_id=current_user.id, scooter_id=scooter.id, price_id=price.id, datetime=curdatetime, completed=0)
        scooter.available = 2
        db.session.add(new_booking)
        db.session.commit()

        durations = {1: "1 hour",
                     4: "4 hours",
                     24: "1 day",
                     168: "1 week"}

        sendConfirmationMessage(username, email, scooter.id, scooter.location, (str(curdatetime.hour)+":"+str(curdatetime.minute)), curdatetime.date(), durations.get(price.duration))
        flash('Scooter booked successfully! Confirmation has been sent via email')
    return render_template("employee.html", form=form, Prices=prices_dict)

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


#page for making new bookings
#calculates discount
@app.route("/booking", methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()

    prices_dict = {}
    prices = models.Prices.query.all()

    discount = 0


    curdatetime = datetime.now()
    date_results = []

    for i in models.Book.query.filter((models.Book.datetime <= curdatetime) & (models.Book.datetime >=  curdatetime - timedelta(days=7))).all():
        if (i.user_id == current_user.id):
            date_results.append(i)

    totalHours = 0
    for i in date_results:
        totalHours += i.duration

    if totalHours > 30 and current_user.staff == 0:
        discount = 0.2

    for p in prices:
        prices_dict[p.duration] = round(p.cost * (1-discount), 2)

    if form.validate_on_submit():
        duration = int(request.form.get('duration'))
        location = request.form.get('location')

        scooter = models.Scooters.query.filter_by(location=location, available=1).first()
        price = models.Prices.query.filter_by(duration=duration).first()


        #check if scooter at the location is free
        if scooter is None:
            flash('No scooter available at location!')
            return render_template("booking.html", form=form, Prices=prices_dict)

        new_booking = models.Book(user_id=current_user.id, scooter_id=scooter.id, price=price.cost*(1-discount), duration=price.duration, datetime=curdatetime, completed=0)
        scooter.available = 2
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('card'))
    return render_template("booking.html", form=form, Prices=prices_dict, discount=discount)

@app.route('/card', methods=['GET', 'POST'])
@login_required
def card():
    form = CardForm()

    new_booking = models.Book.query.filter_by(user_id=current_user.id).order_by(models.Book.id.desc()).first()
    scooter = new_booking.scooters
    price = new_booking.price

    cDetails = []
    for i in models.CardDetails.query.filter_by(user_id=current_user.id):
        cDetails.append(i)

    if form.validate_on_submit():
        number_string = request.form.get('number')
        expiration_date_string = request.form.get('expiration_date')
        security_code = int(request.form.get('security_code'))
        name = request.form.get('name')
        save = request.form.get('save')


        curdatetime = datetime.now()
        success = True

        # Validate card number
        try:
            number_string = number_string.replace(' ', '')
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
            if month not in range(1, 13) or year not in range(curdatetime.year % 1000, 100):
                raise ValueError
            if year == (curdatetime.year % 1000) and month < curdatetime.month:
                raise ValueError
        except ValueError:
            success = False

        # Validate security code
        if security_code not in range(100, 1000):
            success = False

        if not success:
            db.session.delete(new_booking)
            scooter.available = 1
            db.session.commit()
            flash("Payment Unsuccesful, please check card details")
            return redirect(url_for('booking'))

        if save and models.CardDetails.query.filter_by(number=number_string, name=name, security_code=str(security_code), expiration_date=expiration_date_string, user_id=current_user.id) is None:
            cardDetails = models.CardDetails(number=number_string, name=name,
                                            security_code=str(security_code),
                                            expiration_date=expiration_date_string,
                                            user_id=current_user.id
                                            )
            db.session.add(cardDetails)
            db.session.commit()
        durations = {1: "1 hour",
                     4: "4 hours",
                     24: "1 day",
                     168: "1 week"}

        sendConfirmationMessage(current_user.username, current_user.email, scooter.id, scooter.location, (str(curdatetime.hour)+":"+str(curdatetime.minute)), curdatetime.date(), durations.get(new_booking.duration))
        flash('Scooter booked successfully! Please check your email for the Booking Confirmation')
        return redirect(url_for("profile"))
    return render_template("card.html",form=form, Price=price, cardDetails=cDetails)

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
        new_user = models.Users(username=username, age=age, email=email, password=generate_password_hash(password, method='sha256'), staff=0)
        db.session.add(new_user)
        db.session.commit()
        login_user(models.Users.query.filter_by(username = new_user.username).first())
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))
    

#Page for viewing income data
#User inputs day,month,year, and whether the scope should be year/month/week
#Finds all bookings in that time period, 
#returns data in different format for easier processes
@app.route('/price_view', methods=['GET', 'POST'])
def price_view():
    form = monthInputForm()
    time_now = datetime.now()

    total_income = 0
    final_date = ""

    income_Ar = []
    income_DateAr = []

    day = ""
    month = ""
    year = ""
    viewType = "Weekly"
    valid = True
    timeDurations = []
    bookings = []
    scooters = []
    users = []

    #Determines graph data and returns for days and total
    if form.validate_on_submit():
        dateHolder = request.form.get('fullDate').split('-')
        viewType = request.form.get('viewType')

        day = int(dateHolder[2])
        month = int(dateHolder[1])
        year = int(dateHolder[0])
        durations = {1: 0, 4:0, 24:0, 168:0}

        try:
            if (viewType == "Weekly"): #If weekly view
                myDate = datetime(year, month, day)
                final_date = "Week of "+myDate.strftime("%x")
                while(not myDate.strftime("%w") == "0"):
                    myDate = myDate - timedelta(days=1)
                daysOfWeek = ['Monday', "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                for l in range(0, 7):
                    myDate = myDate + timedelta(days=1)
                    date_results = models.Book.query.filter((models.Book.datetime <= myDate) & (models.Book.datetime >=  myDate - timedelta(days=1))).all()
                    temp_val = 0
                    timeDurations.append(durations.copy())
                    for i in date_results:
                        bookings.append(i)
                        scooters.append(models.Scooters.query.get(i.scooter_id))
                        users.append(models.Users.query.get(i.user_id))
                        temp_val += i.price
                        timeDurations[l][i.duration] += i.price

                    total_income += temp_val
                    import calendar
                    income_DateAr.append(daysOfWeek[l])
                    income_Ar.append(temp_val)
                    
            if (viewType == "Monthly"): #If monthly view
                day = ""
                from calendar import monthrange
                length = monthrange(year, month)[1] + 1
                final_date = "Month of "+datetime(year, month, 1).strftime("%d") + "/" + datetime(year, month, 1).strftime("%Y")
                for l in reversed(range(1, length)):
                    myDate = datetime(year, month, length - l)
                    date_results = models.Book.query.filter((models.Book.datetime >= myDate) & (models.Book.datetime <=  myDate + timedelta(days=1))).all()
                    #bookings.append(date_results)
                    temp_val = 0
                    timeDurations.append(durations.copy())
                    for i in date_results:
                        bookings.append(i)
                        scooters.append(models.Scooters.query.get(i.scooter_id))
                        users.append(models.Users.query.get(i.user_id))
                        temp_val += i.price
                        timeDurations[l-1][i.duration] += i.price
                    total_income += temp_val
                    income_DateAr.append(length - l)
                    income_Ar.append(temp_val)
                timeDurations.reverse()

            if (viewType == "Yearly"): #If Yearly view
                day = ""
                month = ""
                myDatec = datetime(year, 1,  1)
                final_date = "Year of "+ datetime(year, 1, 1).strftime("%Y")
                for l in range(1, 13):
                    myDatec = datetime(year, l,  1)
                    if (l+1 == 13):
                        myDate = datetime(year+1, 1,  1)
                    else:
                        myDate = datetime(year, l+1,  1)
                    date_results = models.Book.query.filter((models.Book.datetime <= myDate) & (models.Book.datetime >= myDatec)).all()
                    #bookings.append(date_results)
                    temp_val = 0
                    timeDurations.append(durations.copy())
                    for i in date_results:
                        bookings.append(i)
                        scooters.append(models.Scooters.query.get(i.scooter_id))
                        users.append(models.Users.query.get(i.user_id))
                        temp_val += i.price
                        timeDurations[l-1][i.duration] += i.price
                    total_income += temp_val
                    income_DateAr.append(l)
                    income_Ar.append(temp_val)
        except:
            valid = False


    return render_template("income.html", Scooters=scooters, Users=users, Bookings=bookings, timeDurations=timeDurations, valid = valid, viewType = viewType, final_date=final_date, total_income=total_income, income_Ar=income_Ar, income_DateAr=income_DateAr, year = year, month = month, day = day, form=form)


@app.route("/price", methods=['GET', 'POST'])
def price():
    prices = []
    for i in models.Prices.query.all():
        prices.append(i)
    return render_template("price.html",Prices = prices)
