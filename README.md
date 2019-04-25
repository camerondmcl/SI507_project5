# SI 507 FINAL PROJECT

Cameron McLaughlin

[Link to this repository](https://github.com/camerondmcl/SI507_project5)

---

## Project Description

This project takes data about films from the OMDB API and puts it into a SQLAlchemy database. It uses Flask to display information in a web browser and accept user input to add film data.

## How to run

1. Set up a virtual environments and install all required modules from the included `requirements.txt`.
2. Run the `SI507_project5.py` file from Terminal.
3. Ideally you will be able to operate the Flask application entirely by typing into forms and clicking links/buttons on the webpage, without the need to type anything into the URL bar, but this will depend on whether I am actually able to make that work or not, since I have never tried anything nearly that complex with Flask before.

## How to use

1. A useful instruction goes here
2. A useful second step here
3. (Optional): Markdown syntax to include an screenshot/image: ![alt text](image.jpg)

## Routes in this application
- `/` -> this will be the homepage, which will hopefully have links to each of the other routes as well as a link to a page to add data; each other page will also have a link back to the homepage
- `/movies/all` -> this route will display data for all of the films currently stored in the database
- `/directors/movies` -> this route will display all of the directors currently stored in the database and the films they have directed
- `/directors/studios` -> this route will display all of the directors currently stored in the database and the studios they have worked with

## How to run tests
1. Navigate to the SI507project_tests.py file in Terminal
2. Run the file

## In this repository:
- templates
  - index.html
  - movies_all.html
  - [unknown what/how many templates there will be]
- SI507_project5.py
- SI507project_tests.py
- SI507project_tools.py
- movies_data.db
- README.md
- requirements.txt
- database-diagram.JPG [currently reusing diagram from project 3 because it will be almost the same, but I will most likely add/change a couple things for the Movies table and will update the diagram accordingly]

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [ ] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [ ] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [ ] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [ ] Includes a diagram of your database schema
- [ ] Includes EVERY file needed in order to run the project
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
- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
