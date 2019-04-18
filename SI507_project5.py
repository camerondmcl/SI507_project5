
# import os
import requests
import json
import requests_cache
from flask import Flask, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy

DB_FNAME = 'movies_data.db'
API_KEY = 'd58aa531'
BASE_URL = 'http://www.omdbapi.com/?apikey='

requests_cache.install_cache('movies_cache')
#requests_cache code copied from https://pypi.org/project/requests-cache/

def request_data(base_url, params_dict):
    response = requests.get(base_url, params_dict)
    return response
