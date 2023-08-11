from ..dataContext.sqlAlchemyContext import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(32))
    albums = db.relationship("Album", cascade='all, delete, delete-orphan')