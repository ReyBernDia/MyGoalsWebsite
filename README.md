This is a site where users can register to add, view, and edit their goals. 

## Tech Stack 
**Backend:** Python, Flask, PostgreSQL, SQLAlchemy
**Frontend:** HTML5, Jinja2

## Installation

#### Requirements:

- PostgreSQL
- Python 3.6

To run this app on your local computer, please follow these steps:

Clone repository:
```
$ git clone https://github.com/ReyBernDia/take_home_challenge.git
```
Create and activate your virtual environment:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database 'goals':
```
$ createdb goals
```
In a new terminal window, create relationships in db 'goals':
```
$ python3 -i model.py
$ db.create_all()
```
Run the app from the command line.
```
$ python3 server.py
```