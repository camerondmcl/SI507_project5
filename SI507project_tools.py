# These functions and class definitions are copied from project 3 and will likely stay largely the same but will definitely have some changes made.
import os
import requests
import json
import requests_cache
from flask import Flask, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy

#setting up Flask stuff
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#setting up SQLAlchemy stuff
db = SQLAlchemy(app)
session = db.session
associations = db.Table('associations', db.Column('studio_id', db.Integer, db.ForeignKey('studios.id')), db.Column('director_id', db.Integer, db.ForeignKey('directors.id')))

#data models
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
    movies = db.relationship('Movie', backref='Director')

    def __repr__(self):
        return "{} | {}".format(self.name,self.id)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    genre = db.Column(db.String(64))
    score = db.Column(db.FLOAT)
    rating = db.Column(db.String(10))
    poster_url = db.Column(db.String(250))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'))

    def __repr__(self):
        return "{} | {} | {} | {} | {} | {} | {} | {}".format(self.title,self.year,self.genre,self.score,self.rating,self.poster_url,self.director_id,self.studio_id)

#takes a string as an input, checks whether a studio with that name already exists, returns that studio if so or creates a new one if not
def get_studio(studio_name):
    studio = Studio.query.filter_by(name=studio_name).first()
    if studio:
        return studio
    else:
        new_studio = Studio(name=studio_name)
        session.add(new_studio)
        session.commit()
        return new_studio

#same as above but for directors
def get_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        new_director = Director(name=director_name)
        session.add(new_director)
        session.commit()
        return new_director

#takes a JSON-formatted dictionary in OMDB's format as input and returns a string with the title, director name, and year of release for the purpose of cleanly displaying the data
def get_info(movie_dict):
    return "'{}' directed by {} and released in {}".format(movie_dict['Title'], movie_dict['Director'], movie_dict['Year'])

#takes a dictionary as input and returns a new Movie object from it
def make_new_movie(movie_dict):
    new_movie = Movie(title=movie_dict['Title'], year=int(movie_dict['Year']), genre=movie_dict['Genre'], score=movie_dict['imdbRating'], rating=movie_dict['Rated'], poster_url=movie_dict['Poster'], director_id=get_director(movie_dict['Director']).id, studio_id=get_studio(movie_dict['Production']).id)
    return new_movie

#takes a Movie object as input, makes a query to the database using the movie's title and director id to check if the movie already exists; if it does, it double checks the director_id and if they are identical, it does not add the duplicate; otherwise, it adds the movie to the database; it returns a string that is used in the Flask route to make the Flask code cleaner
def add_new_movie(new_movie):
    movie_same_title = Movie.query.filter_by(title=new_movie.title,director_id=new_movie.director_id).first()
    if movie_same_title:
        if new_movie.director_id == movie_same_title.director_id:
            return ' already exists in the database.'
        else:
            session.add(new_movie)
            session.commit()
            return ' has been added to the database.'
    else:
        session.add(new_movie)
        session.commit()
        return ' has been added to the database.'

#takes a base URL and parameter dictionary and uses Requests and Requests-cache to make and cache API requests; returns a JSON-formatted dictionary
def request_and_process_data(base_url, params_dict):
    response = requests.get(base_url, params_dict)
    return json.loads(response.text)
