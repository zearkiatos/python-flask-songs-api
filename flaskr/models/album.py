from ..dataContext.sqlAlchemyContext import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..utils.EnumToDictionary import EnumToDictionary

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.Integer)
    description = db.Column(db.String(512))
    media = db.Column(db.String(20))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary='album_song', back_populates='albums')
    __table_args__=(db.UniqueConstraint('user', 'title', name='album_title_unique'),)

    def __representation__(self):
        return "{}-{}-{}-{}".format(self.title, self.year, self.description, self.media)
    
class AlbumSchema(SQLAlchemyAutoSchema):
    media = EnumToDictionary(attribute=('media'))
    class Meta:
        model = Album
        include_relationships = True
        load_instance = True