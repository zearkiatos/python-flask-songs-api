from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from ..dataContext import db
from ..models import Song, SongSchema, User, UserSchema, Album, AlbumSchema
from celery import Celery
from config import Config

config = Config()

celery_app = Celery(__name__, broker=f"{config.REDIS_BROKER_BASE_URL}/0")

@celery_app.task(name='log_register')
def log_register(*args):
    pass

song_schema = SongSchema()
user_schema = UserSchema()
album_schema = AlbumSchema()


class SongsView(Resource):
    @jwt_required()
    def get(self):
        return [song_schema.dump(song) for song in Song.query.all()]
    
    @jwt_required()
    def post(self):
        new_song = Song(title=request.json['title'], minutes=request.json['minutes'],
                        seconds=request.json['seconds'], interpreter=request.json['interpreter'])

        db.session.add(new_song)
        db.session.commit()

        return song_schema.dump(new_song)


class SongView(Resource):
    @jwt_required()
    def get(self, song_id):

        return song_schema.dump(Song.query.get_or_404(song_id))
    
    @jwt_required()
    def put(self, song_id):
        song = Song.query.get_or_404(song_id)
        song.title = request.json.get('title', song.title)
        song.minutes = request.json.get('minutes', song.minutes)
        song.seconds = request.json.get('seconds', song.seconds)
        song.interpreter = request.json.get('interpreter', song.interpreter)

        db.session.commit()

        return song_schema.dump(song)
    
    @jwt_required()
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
            args = (username, datetime.utcnow())
            log_register.apply_async(args=args, queue="logs")
            access_token = create_access_token(identity=user[0].id)
            return {"message": "Login session successful", "accessToken": access_token}, 200
        else:
            return {"message": "User name or password wrong"}, 401


class SignInView(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"], password=request.json["password"])
        access_token = create_access_token(identity=request.json['username'])
        db.session.add(new_user)
        db.session.commit()
        return {
            "message": "Created user successful",
            "accessToken": access_token
        }, 201


class UserView(Resource):
    @jwt_required()
    def put(self, user_id):
        try:
            token_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            if token_id == user.id:
                user.password = request.json.get("password", user.password)
                db.session.commit()
                return user_schema.dump(user)
            else:
                return {
                    'message': 'The user is unauthorized',
                }, 401

        except:
            return {
                "message": "Something was wrong",
            }, 500


    @jwt_required()
    def delete(self, user_id):
        try:
            token_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            if token_id == user.id:
                db.session.delete(user)
                db.session.commit()
                return '', 204
            else:
                return {
                    'message': 'The user is unauthorized',
                }, 401
        except:
            return {
                "message": "Something was wrong",
            }, 500


class AlbumsView(Resource):
    @jwt_required()
    def get(self):
        return [album_schema.dump(album) for album in Album.query.all()]

    @jwt_required()
    def post(self):
        new_album = Album(
            title=request.json['title'], year=request.json['year'], description=request.json['description'], media=request.json['media'])

        db.session.add(new_album)
        db.session.commit()

        return album_schema.dump(new_album)


class AlbumView(Resource):
    @jwt_required()
    def get(self, album_id):
        return album_schema.dump(Album.query.get_or_404(album_id))

    @jwt_required()
    def put(self, album_id):
        album = Album.query.get_or_404(album_id)
        album.title = request.json.get('title', album.title)
        album.year = request.json.get('year', album.year)
        album.description = request.json.get('description', album.description)
        album.media = request.json.get('media', album.media)

        db.session.commit()

        return album_schema.dump(album)
    
    @jwt_required()
    def delete(self, album_id):
        album = Album.query.get_or_404(album_id)
        db.session.delete(album)
        db.session.commit()

        return 'The operation was successful', 204


class AlbumsUserView(Resource):
    @jwt_required()
    def post(self, user_id):
        try:
            token_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            if token_id == user.id:
                new_album = Album(title=request.json['title'], year=request.json['year'],
                                description=request.json['description'], media=request.json['media'])
                user = User.query.get_or_404(user_id)
                user.albums.append(new_album)

                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    return 'The user has already had with the name', 409

                return album_schema.dump(new_album)
            else:
                return {
                    'message': 'The user is unauthorized',
                }, 401
        except:
            return {
                "message": "Something was wrong",
            }, 500

    @jwt_required()
    def get(self, user_id):
        try:
            token_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            if token_id == user.id:
                return [album_schema.dump(album) for album in user.albums]
            else:
                return {
                    'message': 'The user is unauthorized',
                }, 401
        except:
            return {
                "message": "Something was wrong",
            }, 500


class SongsAlbumView(Resource):
    @jwt_required()
    def post(self, album_id):
        album = Album.query.get_or_404(album_id)

        if "song_id" in request.json.keys():
            new_song = Song.query.get(request.json["song_id"])
            if new_song is not None:
                album.songs.append(new_song)
                db.session.commit()
            else:
                return 'Wrong song', 404
        else:
            new_song = Song(title=request.json["title"], minutes=request.json["minutes"],
                            seconds=request.json["seconds"], interpreter=request.json["interpreter"])
            album.songs.append(new_song)
        db.session.commit()
        return song_schema.dump(new_song)

    @jwt_required()
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        return [song_schema.dump(song) for song in album.songs]
