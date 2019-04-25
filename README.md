# SI 507 FINAL PROJECT

Cameron McLaughlin

[Link to GitHub repository](https://github.com/camerondmcl/SI507_project5)

---

## Project Description

This project takes data about films from the OMDB API and puts it into a SQLAlchemy database. It uses Flask to display information in a web browser and accept user input to add film data. A sample movies.db is included, but if you wish to start from a clean database you can simply delete, move or rename the file and a new blank one will automatically be created.

## How to run

1. Set up a virtual environments and install all required modules from the included `requirements.txt`.
2. Run the `SI507_project5.py` file from the command line.
3. Open the Flask application in a web browser using the supplied address.
4. From here, you can operate the program entirely through the browser window.

## How to use

1. Click 'Add a film' on the homepage.
2. Type in the title of the film you would like to add. Your search term does not have to match the title exactly, but the closer it is to how the title is written on IMDB, the more likely you are to get the result you are looking for, and any misspellings will likely result in no film being added.
3. You can optionally add the year of release to narrow down results (particularly helpful in cases where there are multiple films with very similar or identical titles, such as 'Titanic' (1997) and 'Titanic' (1953)). The search will still run normally without this parameter and it is not necessary for more specific titles such as 'Pulp Fiction'.
4. Hit 'Submit' when you are ready to run the search. If your search did not return any results, nothing will be added to the database and you will be given the opportunity to run another search or return to the homepage. Otherwise, the first result will automatically be added to the database if it was not yet saved in it. If it was already in the database, a duplicate will not be added.
5. The homepage will display the number of films that are currently stored in the database. From here, you can click 'View all films', 'View all directors', and 'View all studios'.
6. On the 'View all films' page, it will show a list of all films stored in the database with thumbnails of their posters and all data stored about each one.
7. On 'View all directors', there will be a list of all directors stored in the database and each of their films with release years.
8. On 'View all studios', there will be a list of all studios stored in the database and each of the films released by them with release years and directors.

## Routes in this application
- `/` -> the homepage, displaying the number of films saved in the database and with links to add a film and to view all films, directors, and studios
- `/new_movie` -> contains an HTML form where the user can enter the title and (optionally) release year of a film to run a search and add the first result to the database, as well as a link back to the homepage
- `/add_movie` -> route on accessible after performing a search; displays the results of the search and whether the film was added to the database or already existed (or says the search had no results and gives the option to search again) and has a link back to the homepage
- `/all_movies` -> displays data for all films in the database in bulleted format, with a thumbnail of the poster; has a link back to home
- `/all_directors` -> displays all directors stored in the database in bulleted format with each of the films they directed and their release years underneath their names; has a link back to home
- `/all_studios` -> displays all studios stored in the database in bulleted format with each of the films they released and their release years and directors underneath; has a link back to home

## How to run tests
1. Navigate to the SI507project_tests.py file in Terminal
2. Run the file. If everything returns as 'ok' the tests all passed.

## In this repository:
- database-diagram.JPG
- movies.db
- movies_cache.sqlite
- README.md
- requirements.txt
- SI507_project5.py
- SI507project_tests.py
- SI507project_tools.py
- templates
  - add_movie.html
  - all_directors.html
  - all_movies.html
  - all_studios.html
  - index.html
  - new_movie.html

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [ ] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [x] Use of a new module
- [ ] Use of a second new module
- [x] (3?) Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [x] At least one form in your Flask application
- [x] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [ ] Sourcing of data using web scraping
- [x] Sourcing of data using web REST API requests
- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [x] I included a summary of my project and how I thought it went **in my Canvas submission**!
