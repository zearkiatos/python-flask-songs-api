from flaskr import create_app
from flask_restful import Api
from .dataContext.sqlAlchemyContext import db
from .views import SongsView, SongView, SignInView, LogInView, AlbumsView, AlbumView, UserView, AlbumsUserView, SongsAlbumView

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(SongsView, '/songs')
api.add_resource(SongView, '/song/<int:song_id>')
api.add_resource(LogInView, '/login')
api.add_resource(SignInView, '/signin')
api.add_resource(UserView, '/user/<int:user_id>')
api.add_resource(AlbumsView, '/albums')
api.add_resource(AlbumView, '/album/<int:album_id>')
api.add_resource(AlbumsUserView, '/user/<int:user_id>/albums')
api.add_resource(SongsAlbumView, '/album/<int:album_id>/songs')
