from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum
from ..dataContext.sqlAlchemyContext import db
from ..utils.EnumToDictionary import EnumToDictionary

albums_songs = db.Table('album_song',db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True))

class Media(Enum):
    DISK = 1,
    CASSETTE = 2,
    CD = 3

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    interpreter = db.Column(db.String(128))
    albums = db.relationship('Album', secondary='album_song', back_populates='songs')

    def __representation__(self):
        return "{}-{}-{}-{}".format(self.title, self.minutes, self.minutes, self.seconds, self.interpreter)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.Integer)
    description = db.Column(db.String(512))
    media = db.Column(db.Enum(Media))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship(
        'Song', secondary='album_song', back_populates='albums')
    __table_args__ = (db.UniqueConstraint(
        'user', 'title', name='album_title_unique'),)

    def __representation__(self):
        return "{}-{}-{}-{}".format(self.title, self.year, self.description, self.media)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(32))
    albums = db.relationship("Album", cascade='all, delete, delete-orphan')

class SongSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Song
        include_relationships = True
        load_instance = True

class AlbumSchema(SQLAlchemyAutoSchema):
    media = EnumToDictionary(attribute=("media"))

    class Meta:
        model = Album
        include_relationships = True
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = User
        include_relationships = True
        load_instance = True



