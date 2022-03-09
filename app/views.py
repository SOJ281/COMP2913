from flask import Flask, request, redirect, url_for, render_template, flash
from .forms import LoginForm, SignupForm
from app import app, models, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user


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
def booking():
   return render_template("booking.html")


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


