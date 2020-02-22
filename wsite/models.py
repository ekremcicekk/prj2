from wsite import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, timedelta



def turkis_date():
    now = datetime.utcnow()
    next_date = timedelta(hours=3)
    return (now + next_date)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    now = turkis_date()
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    register_date = db.Column(db.DateTime, nullable=False, default=now)
    level = db.Column(db.Integer, nullable=False, default=1)
    score = db.Column(db.Integer, nullable=False, default=0)
    admin = db.Column(db.Boolean, default=False)


    #email reset
    def get_reset_token(self, expires_sec=900):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User: {self.name}, {self.email}"


