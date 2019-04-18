# this file is just in here because I am basing a lot of the classes and basic Flask code off of it. It won't be included in the final project.
import os
from flask import Flask, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

associations = db.Table('associations', db.Column('studio_id', db.Integer, db.ForeignKey('studios.id')), db.Column('director_id', db.Integer, db.ForeignKey('directors.id')))

class Studio(db.Model):
    __tablename__ = 'studios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    directors = db.relationship('Director', secondary=associations, backref=db.backref('studios', lazy='dynamic'), lazy='dynamic')
    movies = db.relationship('Movie', backref='Studio')

    def __repr__(self):
        return "{} | {}".format(self.name,self.id)

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    # studios=db.relationship('Studio', secondary=associations, backref=db.backref('directors', lazy='dynamic'), lazy='dynamic')
    movies = db.relationship('Movie', backref='Director')

    def __repr__(self):
        return "{} | {}".format(self.name,self.id)

class Movie(db.Model):
    # __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True)
    genre = db.Column(db.String(64))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'))

    def __repr__(self):
        return "{}, {} | {}".format(self.name,self.director_id,self.genre)

def get_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        new_director = Director(name=director_name)
        session.add(new_director)
        session.commit()
        return new_director

def get_studio(studio_name):
    studio = Studio.query.filter_by(name=studio_name).first()
    if studio:
        return studio
    else:
        new_studio = Studio(name=studio_name)
        session.add(new_studio)
        session.commit()
        return new_studio

@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    if num_movies == 1:
        return '<h1>1 film saved.</h1>'
    else:
        return '<h1>{} films saved.</h1>'.format(num_movies)

@app.route('/movie/new/<title>/<director>/<genre>/<studio>')
def new_movie(title, director, genre, studio):
    if Movie.query.filter_by(title=title).first():
        return 'That film already exists'
    else:
        director = get_director(director)
        studio = get_studio(studio)
        movie = Movie(title=title, director_id=director.id, genre=genre, studio_id=studio.id)
        session.add(movie)
        session.commit()
        return "New film added: {} - {} - directed by {} - produced by {}".format(movie.title, movie.genre, director.name, studio.name)

@app.route('/movies/all')
def all_movies():
    movies_lst = []
    movies = Movie.query.all()
    for movie in movies:
        new_movie = []
        new_movie.append(movie.title)
        new_movie.append(Director.query.filter_by(id=movie.director_id).first().name)
        new_movie.append(Studio.query.filter_by(id=movie.studio_id).first().name)
        movies_lst.append(new_movie)
    return render_template('all_movies.html', all_movies=movies_lst)

@app.route('/studios/all')
def all_studios():
    studios_lst = []
    studios = Studio.query.all()
    for studio in studios:
        new_studio = []
        new_studio.append(studio.name)
        studios_movies = []
        movies = Movie.query.all()
        for movie in movies:
            if new_studio[0] == Studio.query.filter_by(id=movie.studio_id).first().name:
                studios_movies.append(movie.title)
        new_studio.append(studios_movies)
        studios_lst.append(new_studio)
    return render_template('all_studios.html', all_studios=studios_lst)

@app.route('/directors/all')
def all_directors():
    directors_lst = []
    directors = Director.query.all()
    for director in directors:
        new_director = []
        new_director.append(director.name)
        directors_movies = []
        movies = Movie.query.all()
        for movie in movies:
            if new_director[0] == Director.query.filter_by(id=movie.director_id).first().name:
                directors_movies.append(movie.title)
        new_director.append(directors_movies)
        directors_lst.append(new_director)
    return render_template('all_directors.html', all_directors=directors_lst)

@app.route('/studio/<old_name>/<new_name>')
def change_studio(old_name, new_name):
    studio = Studio.query.filter_by(name=old_name).first()
    studio.name = new_name
    return '{} has been renamed to {}'.format(old_name, studio.name)

@app.route('/movie/<old_title>/<new_title>')
def change_movie(old_title, new_title):
    movie = Movie.query.filter_by(title=old_title).first()
    movie.title = new_title
    return '{} has been retitled to {}'.format(old_title, movie.title)

@app.route('/director/<old_name>/<new_name>')
def change_director(old_name, new_name):
    director = Director.query.filter_by(name=old_name).first()
    director.name = new_name
    return '{} has been renamed to {}'.format(old_name, director.name)

if __name__ == '__main__':
    db.create_all()
    app.run()
