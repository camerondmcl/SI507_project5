
# import sys
import os
import requests
import json
import requests_cache
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from SI507project_tools import *

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

DB_FNAME = 'movies.db'
API_KEY = 'd58aa531'
BASE_URL = 'http://www.omdbapi.com/'

requests_cache.install_cache('movies_cache')
#requests_cache code copied from https://pypi.org/project/requests-cache/

# test_url = BASE_URL
# test_dict = {'t':'Titanic', 'apikey':API_KEY}
# test_response = request_and_process_data(test_url, test_dict)
# print(test_response)
# movie = make_new_movie(test_response)
# print(add_movie(movie))
# print(movie)
# dict_2 = {'t':'Star Wars Episode IV: A New Hope', 'apikey':API_KEY}
# response_2 = request_and_process_data(test_url, dict_2)
# print(response_2)
# movie_2 = make_new_movie(response_2)
# print(add_movie(movie_2))
# print(movie_2)

# print(SI507project_tools.__file__)
# print(os.getcwd())

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

# @app.route('/show_result',methods=["GET"])
# def show_result():
#     if request.method == "GET":
#         title = request.args.get('t', '')
#         year = request.args.get('y', '')
#         request_dict = {'t':title, 'y':year, 'apikey':API_KEY}
#         response = request_and_process_data(BASE_URL, request_dict)
#         # response_dict = json.loads(response)
#     return render_template('show_result.html', movie_data = get_info(response), title=title, year=year)

@app.route('/add_movie',methods=["GET"])
def add_movie():
    """if request.method == "GET":
        movie_data = request.args.get('response')
        #print(movie_data)
    # return 'Film added to database!<br><a href="/">Return to home</a>'"""
    if request.method == "GET":
        # title = request.args.get('t', '')
        # year = request.args.get('y', '')
        request_dict = {'t':request.args.get('t', ''), 'y':request.args.get('y', ''), 'apikey':API_KEY}
        response = request_and_process_data(BASE_URL, request_dict)
        # return str(response)
        try:
            movie = make_new_movie(response)
            added = add_new_movie(movie)
        # if result == 0:
        #     added = ' has been added to the database.'
        # else:
        #     added = ' already exists in the database.'
            return render_template('add_movie.html', movie_data=get_info(response), added=added)
        except:
            return 'Your search did not match any results.<br><br><a href="/new_movie">Run another search</a><br><br><a href="/">Return to home</a>'

@app.route('/all_movies')
def all_movies():
    movies_lst = []
    movies = Movie.query.all()
    for movie in movies:
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
        for movie in movies:
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
        for movie in movies:
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
