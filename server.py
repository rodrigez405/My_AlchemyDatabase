"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask,render_template, redirect, request, flash, session
from model import User, Rating, Movie, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension






app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/movie_list")   
def movie_list():

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movies_list.html", movies=movies)


@app.route("/movies_list/<int:id>")
def movie_details(id): 
    """ MOVIE DETAILS"""
    movie = Movie.query.get(id)
    print movie
    movie_title = movie.title
    print movie_title
    ratings_list = movie.ratings 
    return render_template("movie_details.html", movie_title=movie_title, ratings=ratings_list, movie_id=id)

@app.route("/sign_in", methods=["POST", "GET"])
def login():
    """Login."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.query(User).filter(User.email == email).one()
        if password != user.password: 
            # import pdb; pdb.set_trace()
            flash('Invalid credentials, try again')
            return render_template("login.html")
        else:    
            session['user_id'] = user.user_id
            flash('You were successfully logged in')
            id = str(session['user_id'])
            return redirect("/users/" + id)       
    else: 
        return render_template("login.html") 

@app.route("/sign_out")
def logout():
    """ LOGOUT."""
    if "user_id" in session: 
        session.pop('user_id', None)
        flash('You have been logged out')
        return render_template('homepage.html')
    else: 
        flash('Are you sure you logged in?')
        return render_template('login.html')

@app.route("/users/<int:id>")
def users_details(id):
    """ USER DETAILS"""
    user = User.query.get(id)
    age = user.age
    zipcode = user.zipcode
    movie_list = user.ratings
    return render_template("user_details.html", age=age, zipcode=zipcode, movie_list=movie_list)


@app.route("/rate_movie/<int:id>")
def rate_movie(id):

    updated_score = request.args.get("rating")
    print '************************************', session

    if session.get('user_id', None): 
        user_id = session['user_id'] 
        rating = Rating.query.filter(Rating.movie_id == id, Rating.user_id == user_id).all()
        if rating: 
            print rating
            rating[0].score = updated_score
            db.session.commit()
            flash("your score has been updated!")
        else: 
            new_rating = Rating(movie_id=id, user_id=user_id, score=updated_score)
            db.session.add(new_rating)
            db.session.commit()
            flash("your score has been added! thanks for scoring")
    else: 
        flash("are you sure you are logged in? ")

    return render_template("homepage.html")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()