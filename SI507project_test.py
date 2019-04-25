import sqlite3
import unittest
from SI507_project5 import *
# test code was copied and modified from a lecture example

API_KEY = 'd58aa531'
BASE_URL = 'http://www.omdbapi.com/'
PARAMS = {'t':'titanic', 'y':'1997', 'apikey':API_KEY}
TEST_JSON = {
  "Response": "True",
  "Title": "Titanic",
  "Year": "1997",
  "Rated": "PG-13",
  "Released": "19 Dec 1997",
  "Runtime": "194 min",
  "Genre": "Drama, Romance",
  "Director": "James Cameron",
  "Writer": "James Cameron",
  "Actors": "Leonardo DiCaprio, Kate Winslet, Billy Zane, Kathy Bates",
  "Plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
  "Language": "English, Swedish, Italian",
  "Country": "USA",
  "Awards": "Won 11 Oscars. Another 111 wins & 77 nominations.",
  "Poster": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
  "Ratings": [
    {
      "Source": "Internet Movie Database",
      "Value": "7.8/10"
    },
    {
      "Source": "Rotten Tomatoes",
      "Value": "89%"
    },
    {
      "Source": "Metacritic",
      "Value": "75/100"
    }
  ],
  "Metascore": "75",
  "imdbRating": "7.8",
  "imdbVotes": "946,032",
  "imdbID": "tt0120338",
  "Type": "movie",
  "DVD": "10 Sep 2012",
  "BoxOffice": "N/A",
  "Production": "Paramount Pictures",
  "Website": "http://www.titanicmovie.com/"
}
# ^ a sample JSON response object from OMDB, formatted into a dictionary the way the request_and_process_data() function is supposed to

class HW5SQLiteDBTests(unittest.TestCase):

	def setUp(self):
		self.conn = sqlite3.connect("movies.db")
		self.cur = self.conn.cursor()

	def test_check_db(self):
		self.cur.execute("select * from movies")
		data = self.cur.fetchone()
		self.assertEqual(len(data), 9, "Testing to make sure movies table exists")

	def test_make_movie(self):
		test_movie = make_new_movie(TEST_JSON)
		self.assertEqual(test_movie.title, "Titanic", "Testing to make sure make_new_movie finds title from JSON input")

	def test_request(self):
		movie_data = request_and_process_data(BASE_URL, PARAMS)
		self.assertEqual(type(movie_data), type(TEST_JSON), "Testing to make sure request_and_process_data returns the correct type")

	def test_get_info(self):
		movie_str = get_info(TEST_JSON)
		self.assertEqual(movie_str, "'Titanic' directed by James Cameron and released in 1997", "Testing to make sure get_info returns the correct string")

	def tearDown(self):
		self.conn.commit()
		self.conn.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
