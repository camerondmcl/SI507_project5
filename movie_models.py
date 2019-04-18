
from SI507_project3 import *
from flask_sqlalchemy import SQLAlchemy

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
