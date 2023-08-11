from ..dataContext.sqlAlchemyContext import db

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.Integer)
    description = db.Column(db.String(512))
    media = db.Column(db.String(20))

    def __representation__(self):
        return "{}-{}-{}-{}".format(self.title, self.year, self.description, self.media)