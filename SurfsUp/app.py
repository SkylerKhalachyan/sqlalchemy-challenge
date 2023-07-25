# Import the dependencies.
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Text


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
## Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#From Day 3 Activity 4
# @app.route("/")
# def home():
    # print("Server received request for 'Home' page...")
    # return "Welcome to my 'Home' page!" 

# 1 "/"
@app.route('/')
def home():
    print("Server received request for 'Home' page...")
    return "Home Page"

#2 "/api/v1.0/precipitation"
@app.route('/api/v1.0/precipitation')
def precipitation():

    print("Server received request for 'precipitation' page...")
    return 

#3 "/api/v1.0/stations"
@app.route('/api/v1.0/stations')
def stations():

    print("Server revceived request for 'stations' page...")
    return

#4 "/api/v1.0/tobs"
@app.route('/api/v1.0/tobs')
def tobs():

    print("Server received request for 'tobs' page...")
    return










# Best practice to keep this piece included
if __name__ == "__main__":
    # to run Flask app
    app.run(debug=True)