from index import db
from sqlalchemy.sql import func

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    package = db.Column(db.String(8))
    start_time = db.Column(db.DateTime, default=func.now())
    end_time = db.Column(db.DateTime)
