from . import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(200), default="...", unique=True)
    message = db.Column(db.Text, nullable=True)
    package = db.Column(db.String(8))
    start_time = db.Column(db.DateTime, default=func.now())
    end_time = db.Column(db.DateTime)
    last_changed_message = db.Column(db.DateTime, nullable=True)
    bots = db.relationship("Bot")

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String)
    user_id = db.Column(db.String(200), db.ForeignKey("user.username"))
