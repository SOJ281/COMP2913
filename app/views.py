from flask import Flask, request, redirect, url_for, render_template
from forms import LoginForm, SignupForm

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        # get and check input login information form, if true then redirect to the homepage
        if form.validate():
            email = form.email.data
            password = form.password.data
            return redirect("/staff")
        else:
            return "Your input format is wrong!"


@app.route("/staff", methods=['GET', 'POST'])
def staff():
    if request.method == 'GET':
       return render_template("staff.html")


@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
       return render_template("user.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'GET':
       return render_template("signup.html")
    else:
        # get and check input login information form, if true then signup successfully
        if form.validate():
            name = form.name.data
            age = form.age.data
            email = form.email.data
            password = form.password.data
            return "signup successfully!"
        else:
            return "Your input format is wrong!"


if __name__ == '__main__':
    app.run()
