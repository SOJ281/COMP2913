WTF_CSRF_ENABLED = True

SECRET_KEY = 'sekret-keyy'

import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABSE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLACHEMY_TRACK_MODIFACTIONS = True
