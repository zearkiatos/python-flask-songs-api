from ..dataContext.sqlAlchemyContext import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    interpreter = db.Column(db.String(128))
    albums = db.relationship('Album', secondary="album_song", back_populates='songs')

    def __representation__(self):
        return "{}-{}-{}-{}".format(self.title, self.minutes, self.minutes, self.seconds, self.interpreter)