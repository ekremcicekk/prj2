from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b89ee54abbd28728736db3a53207d6d6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wdatabase.db'
#gmail-e-posta-ayar

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kisisellestirilmisogrenme@gmail.com'
app.config['MAIL_PASSWORD'] = '44=?1923'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#db = SQLAlchemy(app)
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
mail=Mail(app)

from wsite import routes

