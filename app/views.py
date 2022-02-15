from flask import Flask, render_template, redirect, url_for, request, flash
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html', title="Base Page")
