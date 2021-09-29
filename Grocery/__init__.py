
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///grocery.db'
app.config['SECRET_KEY']='74e027ea16294a0f557476a8'
db=SQLAlchemy(app)

bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
from Grocery import route  