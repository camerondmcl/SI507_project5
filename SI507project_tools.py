# These functions and class definitions are copied from project 3 and will likely stay largely the same but will definitely have some changes made.
from flask_sqlalchemy import SQLAlchemy

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
