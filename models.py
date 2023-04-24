from . import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    message = db.Column(db.Text, nullable=True)
    package = db.Column(db.String(8))
    start_time = db.Column(db.DateTime, default=func.now())
    end_time = db.Column(db.DateTime)
