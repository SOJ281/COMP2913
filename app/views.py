from flask import Flask, render_template, redirect, url_for, request, flash
from app import app
from .forms import SignupForm, LoginForm

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html', title="Base Page")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
