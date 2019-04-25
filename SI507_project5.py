
import os
import requests
import json
import requests_cache
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from SI507project_tools import *

DB_FNAME = 'movies.db'
API_KEY = 'd58aa531'
BASE_URL = 'http://www.omdbapi.com/'

requests_cache.install_cache('movies_cache')
#requests_cache code copied from https://pypi.org/project/requests-cache/

@app.route('/')
def index():
    movies = Movie.query.all()
    num = len(movies)
    if num == 1:
        num_movies = '1 film'
    else:
        num_movies = '{} films'.format(num)
    return render_template('index.html', num_movies=num_movies)

@app.route('/new_movie')
def new_movie():
    return render_template('new_movie.html')

@app.route('/add_movie',methods=["GET"])
def add_movie():
    if request.method == "GET":
        request_dict = {'t':request.args.get('t', ''), 'y':request.args.get('y', ''), 'apikey':API_KEY}
        response = request_and_process_data(BASE_URL, request_dict)
        try: #tries to make a Movie object out of the response data and add it to the database
            movie = make_new_movie(response)
            added = add_new_movie(movie)
            return render_template('add_movie.html', movie_data=get_info(response), added=added)
        except: #runs if there was not a valid response object, i.e. the search did not match any entries on OMDB
            return 'Your search did not match any results.<br><br><a href="/new_movie">Run another search</a><br><br><a href="/">Return to home</a>'

@app.route('/all_movies')
def all_movies():
    movies_lst = []
    movies = Movie.query.all()
    for movie in movies: #these next 3 routes use nested lists to store movie data because that seemed like the easiest way to make it work with HTML to display in Flask
        new_movie = []
        new_movie.append(movie.poster_url)
        new_movie.append(movie.title)
        new_movie.append(movie.year)
        new_movie.append(Director.query.filter_by(id=movie.director_id).first().name)
        new_movie.append(Studio.query.filter_by(id=movie.studio_id).first().name)
        new_movie.append(movie.score)
        new_movie.append(movie.rating)
        new_movie.append(movie.genre)
        movies_lst.append(new_movie)
    return render_template('all_movies.html', all_movies=movies_lst)

@app.route('/all_directors')
def all_directors():
    directors_lst = []
    directors = Director.query.all()
    for director in directors:
        new_director = []
        new_director.append(director.name)
        directors_movies = []
        movies = Movie.query.all()
        for movie in movies: #searches all movies and saves data from them if the director_id matches
            if new_director[0] == Director.query.filter_by(id=movie.director_id).first().name:
                movie_and_year = movie.title + ', ' + str(movie.year)
                directors_movies.append(movie_and_year)
        new_director.append(directors_movies)
        directors_lst.append(new_director)
    return render_template('all_directors.html', all_directors=directors_lst)

@app.route('/all_studios')
def all_studios():
    studios_lst = []
    studios = Studio.query.all()
    for studio in studios:
        new_studio = []
        new_studio.append(studio.name)
        studios_movies = []
        movies = Movie.query.all()
        for movie in movies: #searches all movies and saves data from them if the studio_id matches
            if new_studio[0] == Studio.query.filter_by(id=movie.studio_id).first().name:
                director_name = Director.query.filter_by(id=movie.director_id).first().name
                movie_and_year = movie.title + ' (' + str(movie.year) + '), directed by ' + director_name
                studios_movies.append(movie_and_year)
        new_studio.append(studios_movies)
        studios_lst.append(new_studio)
    return render_template('all_studios.html', all_studios=studios_lst)

if __name__ == '__main__':
    db.create_all()
    app.run()
