import sqlite3
import unittest
from SI507_project5 import *
# I am aware that these tests are written for SQLite (because they are copied from HW5) and my project is using SQLAlchemy. From the vague understanding I currently have of SQL and some brief reading I did tonight it seems like SQLite commands should still work, but I fully expect to have to fix and rewrite large portions of this file once I have actually written more of the main code. I might have to get help in office hours with changing it from SQLite to SQLAlchemy if that is necessary.

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
} #a sample JSON response object from OMDB

class HW5SQLiteDBTests(unittest.TestCase):

	def setUp(self):
		self.conn = sqlite3.connect("movies.db")
		self.cur = self.conn.cursor()

	def check_db(self):
		self.cur.execute("select * from movies")
		data = self.cur.fetchone()
		self.assertEqual(len(data), 9, "Testing to make sure movies table exists")

	# def test_get_movie(self):
	# 	test_movie_dict = {}
	#
	def test_make_movie(self):
		test_movie = make_new_movie(TEST_JSON)
		self.assertEqual(test_movie.title, "Titanic", "Testing to make sure make_new_movie finds title from JSON input")

	# def test_for_movies_table(self):
	# 	self.cur.execute("select title, genre, director, studio, score, rating from movies where title = 'Pulp Fiction'")
	# 	data = self.cur.fetchone()
	# 	self.assertEqual(data,('Pulp Fiction', 'Crime', 'Quentin Tarantino', 'Miramax', 8.9, 'R'), "Testing data that results from selecting movie Pulp Fiction")
	#
	# def test_movie_insert_works(self):
	# 	movie = ('Titanic', 'Drama', 'James Cameron', 'Twentieth Century Fox', 7.8, 'PG-13')
	# 	mv = ('Titanic', 'Drama', 'James Cameron', 'Twentieth Century Fox', 7.8, 'PG-13')
	# 	self.cur.execute("insert into movies(title, genre, director, studio, score, rating) values (?, ?, (select id from directors where name=?), (select id from studios where name=?), ?, ?)", movie)
	# 	self.conn.commit()
	#
	# 	self.cur.execute("select title, genre, director, studio, score, rating from movies where title= 'Titanic'")
	# 	data = self.cur.fetchone()
	# 	self.assertEqual(data,mv,"Testing another select statement after a sample insertion")
	#
	# def test_for_movies_table(self):
	# 	res = self.cur.execute("select * from movies")
	# 	data = res.fetchall()
	# 	self.assertTrue(data, 'Testing that you get a result from making a query to the movies table')
	#
	# def test_director_insert_works(self):
	# 	# I am unsure if this test will work because I do not know how self-increasing IDs or adding entries for relationship databases works here and will have to figure that out later
	# 	director = ('Steven Spielberg')
	# 	self.cur.execute("insert into directors(id, name, movies) values (?, ?, (select id from movies where director_id=?))", director)
	# 	self.conn.commit()
	#
	# 	self.cur.execute("select id, name, movies from directors where name = 'Steven Spielberg'")
	# 	data = self.cur.fetchone()
	# 	self.assertEqual(data, director, "Testing a select statement where name = Steven Spielberg")
	#
	#
	# def test_foreign_key_movies(self):
	# 	res = self.cur.execute("select * from movies INNER JOIN directors ON movies.director = director.id")
	# 	data = res.fetchall()
	# 	self.assertTrue(data, "Testing that result of selecting based on relationship between movies and directors does work")
	# 	# I don't understand what the list in this next line is for and will have to figure that out
	# 	self.assertTrue(len(data) in [1795, 1796], "Testing that there is in fact the amount of data entered that there should have been -- based on this query of everything in both tables.{}".format(len(data)))


	def tearDown(self):
		self.conn.commit()
		self.conn.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
