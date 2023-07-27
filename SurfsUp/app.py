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

# 1 "/"
@app.route('/')
def home():
    print("Server received request for 'Home' page...")
    return ("<h1>Welcome to my home page<h1/><br/>"
            "The available routes are: <br/>"
            "/api/v1.0/precipitation <br/>"
            "/api/v1.0/stations <br/>"
            "/api/v1.0/tobs <br/>"
            "/api/v1.0/&lt;start&gt; <br/>"
            "/api/v1.0/<start>/<end>"
            )




#2 "/api/v1.0/precipitation"
@app.route('/api/v1.0/precipitation')
def precipitation():
# Create a dictionary to hold precipitation values
# Perform a query to retrieve the data and precipitation scores
# Find the most recent date in the data set.

    most_recent_date_str = session.query(func.max(Measurement.date))\
        .scalar()
    most_recent_date_str
# Starting from the most recent data point in the database. 
    most_recent_date = dt.date.fromisoformat(most_recent_date_str)
# Calculate the date one year from the last date in data set.
    beginning_of_period = most_recent_date - dt.timedelta(days=365) 

    date_precip_one_year = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= beginning_of_period)\
        .all()

    session.close()

    precip_data = []

    for date, prcp in date_precip_one_year:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_data.append(precip_dict)

    print("Server received request for 'precipitation' page...")
    return jsonify(precip_data)



#3 "/api/v1.0/stations"
@app.route('/api/v1.0/stations')
def stations():
    # return a list of all stations
    stations_tuple = session.query(Measurement.station).group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()
    stations_list = []
    # create list from tuple values
    for val in stations_tuple:
        stations_list.append(val[0])
    # close session
    session.close()
    print("Server revceived request for 'stations' page...")
    return jsonify(stations_list)

#4 "/api/v1.0/tobs"
@app.route('/api/v1.0/tobs')
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_route_q = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281',\
           Measurement.date > year_ago).all()
    session.close()

    tobs_list = list(np.ravel(tobs_route_q))
   
    print("Server received request for 'tobs' page...")
    return jsonify(tobs_list)

#5 "/api/v1.0/<start>"
#6 "/api/v1.0/<start>/<end>"
#Input only start date 
@app.route('/api/v1.0/<start>')
#Input both start and end date
@app.route('/api/v1.0/<start>/<end>')
# Typing code into the parenthesis because these are inputs. The end 
# date will not always be input, we want to default this date to the most recent date. 
# The end date can be overwritten by the end user input.
# Whatever you input into the parenthesis is a variable.
# This must match exactly, later within the scope of the function. 
def stats(start, end=dt.date.max.isoformat()):
    sel = [func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
# *sel grabs above
    tobs_stats = session.query(*sel)\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .first()
    
    session.close()

    return jsonify(list(tobs_stats))



# Best practice to keep this piece included
if __name__ == "__main__":
    # to run Flask app
    app.run(debug=True)