from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

csrf = CSRFProtect(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)

login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.init_app(app)

from app import views, models

# for now the login function will be just for the user
# staff will be added later
@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(user_id)






