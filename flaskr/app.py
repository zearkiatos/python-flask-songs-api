from flaskr import create_app
from .dataContext import db
from .models import Song, Media, Album

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

#Test
with app.app_context():
    song = Song(title='Nothing else Matters', minutes=6,seconds=25, interpreter="Metallica")
    song2 = Song(title='November Rain 🌧️', minutes=12,seconds=10, interpreter="Guns n' Roses")
    album = Album(title='Black Album', year=1992, description="Metallica black album", media=Media.CD.name)
    db.session.add(song)
    db.session.commit()
    db.session.add(song2)
    db.session.commit()
    db.session.add(album)
    db.session.commit()
    print(Song.query.all())