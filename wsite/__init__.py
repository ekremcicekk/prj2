from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b89ee54abbd28728736db3a53207d6d6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wdatabase.db'


# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kisisellestirilmisogrenme@gmail.com'
app.config['MAIL_PASSWORD'] = '44=?1923'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


db = SQLAlchemy(app)
# db = SQLAlchemy()
# db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' #login değilse yönlendirilecek sayfa tepml.
login_manager.login_message = "Bu sayfaya erişmek için lütfen giriş yapın."
login_manager.login_message_category = 'info'


mail=Mail(app)
bcrypt = Bcrypt(app)


from wsite import routes
