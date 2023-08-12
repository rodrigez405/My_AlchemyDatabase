"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy



def load_users():
    """Load users from u.user into database."""

    lines = [line.rstrip('\n') for line in open("seed_data/u.user")]

    for line in lines: 
        column_data = line.split("|")
        line = User(age=column_data[1], zipcode=column_data[4])
        db.session.add(line)
    db.session.commit()


        
def load_movies():
    """Load movies from u.item into database."""
    lines = [line.rstrip('\n') for line in open("seed_data/u.item")]    
    for line in lines: 
        column_data = line.split("|")
        title = column_data[1]
        new_title = title[:-7]
    
        date_string = column_data[2]
        if date_string is not '':
            column_date = datetime.strptime(date_string, '%d-%b-%Y')
            line = Movie(movie_id=column_data[0], title=new_title, released_at=column_date, imdb_url=column_data[4])
        else: 
            line = Movie(movie_id=column_data[0], title=new_title, imdb_url=column_data[4])
            

        db.session.add(line)
    db.session.commit()




def load_ratings():
    """Load ratings from u.data into database."""

    lines = [line.rstrip('\n') for line in open("seed_data/u.data")]

    for line in lines: 
        column_data = line.split("\t")
        line = Rating(movie_id=column_data[1], user_id=column_data[0], score=column_data[2])
        db.session.add(line)
    db.session.commit()
  





if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
