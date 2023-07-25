# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Text
import numpy as np
import pandas as pd
import datetime as dt


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

# Create a dictionary to hold precipitation values
# precip = {"date":"prcp"}

# Perform a query to retrieve the data and precipitation scores

date_precip_one_year = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= beginning_of_period)\
    .all()


# Save the query results as a Pandas DataFrame. Explicitly set the column names

date_precip_df = pd.DataFrame(date_precip_one_year)
date_precip_df

date_precip_df.rename(columns={0:"Date",1:"Precipitation"},inplace=True)
date_precip_df

# Sort the dataframe by date

date_precip_df.sort_values(by='Date', ascending =True, inplace=True)
date_precip_df

precip = date_precip_df.to_dict(precip)

# 1 "/"
@app.route('/')
def home():
    print("Server received request for 'Home' page...")
    return ("<h1>Home Page<h1/><br/>"
            "The available routes are: <br/>"
            "/api/v1.0/precipitation <br/>"
            "/api/v1.0/stations <br/>"
            "/api/v1.0/tobs"

#2 "/api/v1.0/precipitation"
@app.route('/api/v1.0/precipitation')
def precipitation():

    print("Server received request for 'precipitation' page...")
    return jsonify(precip)

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

#5 "/api/v1.0/<start>"
@app.route('/api/v1.0/<start>')
def start():

    print("Server received request for 'start' page...")
    return
#6 "/api/v1.0/<start>/<end>"
@app.route('/api/v1.0/<start>/<end>')
def startend():

    print("Server received request for 'startend' page...")
    return








# Best practice to keep this piece included
if __name__ == "__main__":
    # to run Flask app
    app.run(debug=True)