from flaskr import create_app
from .dataContext.sqlAlchemyContext import db
from .models import Media, Album, User, Song

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

#Test
with app.app_context():
    user = User(username='zearkiatos', password='p@$$w0rd')
    album = Album(title='Black Album', year=1992, description="Metallica black album", media=Media.CD.name)
    song = Song(title="Nothing else matter", minutes=6, seconds=40, interpreter='Metallica')
    user.albums.append(album)
    album.songs.append(song)
    db.session.add(user)
    db.session.add(song)
    db.session.commit()
    print(User.query.all())
    print(User.query.all()[0].albums)
    print(Album.query.all()[0].songs)
    print(Song.query.all())
    print(Album.query.all())
    db.session.delete(album)
    print(User.query.all())
    print(Album.query.all())
    print(Song.query.all())
    print(Album.query.all())