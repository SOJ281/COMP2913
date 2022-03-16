from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/first_item')
def first_item():
    return render_template('first item.html')


@app.route('/second_item')
def second_item():
    return render_template('second item.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


if __name__ == '__main__':
    app.run()
