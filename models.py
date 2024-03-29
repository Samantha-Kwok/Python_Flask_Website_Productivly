from datetime import datetime
from todolist import db,login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), unique=True , nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    tasks=db.relationship('Task', backref="owner", lazy=True)
    posts=db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
    def get_reset_token(self, expires_sec=1800):
        s=Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id":self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s=s=Serializer(current_app.config["SECRET_KEY"])
        try: 
            user_id=s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


class Task(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    item=db.Column(db.String(200),nullable=False)
    category= db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False,)
    complete= db.Column(db.Boolean, nullable=False, unique=False, default=False)
    date_created=db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    actual_completion_date=db.Column(db.Date)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.item}', '{self.category}', '{self.start_date}', '{self.end_date}', '{self.complete}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    subtitle=db.Column(db.String(500), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    post_image= db.Column(db.String(20), nullable=False, default="newdefaultimage.jpg")
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.post_image}')"

    

    
