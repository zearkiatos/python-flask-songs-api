from flask_restful import Resource
from flask import request
from ..dataContext import db
from ..models import Song, SongSchema, User, UserSchema, Album, AlbumSchema

song_schema = SongSchema()
user_schema = UserSchema()
album_schema = AlbumSchema()


class SongsView(Resource):
    def get(self):
        return [song_schema.dump(song) for song in Song.query.all()]

    def post(self):
        new_song = Song(title=request.json['title'], minutes=request.json['minutes'],
                        seconds=request.json['seconds'], interpreter=request.json['interpreter'])

        db.session.add(new_song)
        db.session.commit()

        return song_schema.dump(new_song)


class SongView(Resource):

    def get(self, song_id):

        return song_schema.dump(Song.query.get_or_404(song_id))

    def put(self, song_id):
        song = Song.query.get_or_404(song_id)
        song.title = request.json.get('title', song.title)
        song.minutes = request.json.get('minutes', song.minutes)
        song.seconds = request.json.get('seconds', song.seconds)
        song.interpreter = request.json.get('interpreter', song.interpreter)

        db.session.commit()

        return song_schema.dump(song)

    def delete(self, song_id):
        song = Song.query.get_or_404(song_id)
        db.session.delete(song)
        db.session.commit()

        return 'The operation was successful', 204


class LogInView(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username, password=password).all()
        if user:
            return {"message": "Login session successful"}, 200
        else:
            return {"message": "User name or password wrong"}, 401


class SignInView(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"], password=request.json["password"])
        db.session.add(new_user)
        db.session.commit()
        return "Created user successful", 201
    
class UserView(Resource):
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.password = request.json.get("password", user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class AlbumsView(Resource):
    def get(self):
        return [album_schema.dump(album) for album in Album.query.all()]

    def post(self):
        new_album = Album(
            title=request.json['title'], year=request.json['year'], description=request.json['description'], media=request.json['media'])

        db.session.add(new_album)
        db.session.commit()

        return album_schema.dump(new_album)


class AlbumView(Resource):

    def get(self, album_id):
        return album_schema.dump(Album.query.get_or_404(album_id))

    def put(self, album_id):
        album = Album.query.get_or_404(album_id)
        album.title = request.json.get('title', album.title)
        album.year = request.json.get('year', album.year)
        album.description = request.json.get('description', album.description)
        album.media = request.json.get('media', album.media)

        db.session.commit()

        return album_schema.dump(album)

    def delete(self, album_id):
        album = Album.query.get_or_404(album_id)
        db.session.delete(album)
        db.session.commit()

        return 'The operation was successful', 204
