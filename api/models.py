from .index import db

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
