from ..dataContext.sqlAlchemyContext import db

albums_songs = db.Table('album_song',db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True))