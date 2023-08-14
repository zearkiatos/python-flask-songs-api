from flaskr import create_app
from .dataContext.sqlAlchemyContext import db
from .models import Media, Album, User, Song, AlbumSchema

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

#Test
with app.app_context():
    album_schema = AlbumSchema()
    album = Album(title='Black Album', year=1992, description="Metallica black album", media=Media.CD)
    db.session.add(album)
    db.session.commit()
    print(Album.query.all())
    # print(album_schema.dumps(album) for album in Album.query.all())