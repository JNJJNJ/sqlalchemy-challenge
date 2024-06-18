# Import the dependencies.

import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

import json

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///sqlalchemy-challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

measurement = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#1. 
#-Start at the homepage
#-List all the available routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end>"    
    )

#2. Convert query results
#- Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#- Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query
    precip_data = session.query(measurement.date,measurement.prcp).filter(measurement.date >= dt.date(2017,8,23)).order_by(measurement.date.desc()).all()
    total_precip = []
    for date, prcp in precip_data:
        precip_dict = {}
        precip_dict[date] = prcp
        total_precip.append(precip_dict)

    #Close session
    session.close()

    #Return JSON
    return jsonify(total_precip)


#3. Return JSON list
#- Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query
    stations_data = session.query(Station.station).all()

    total_stations = list(np.ravel(stations_data))

    #Close session
    session.close()

    #Return JSON
    return jsonify(total_stations)



#4. Query dates and temps, return JSON of last year temps.
#- Query the dates and temperature observations of the most-active station for the previous year of data.
#- Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query
    tobs_data = session.query(measurement.date,measurement.tobs).filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= (2017,8,23)).all()
    
    total_tobs = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        total_tobs.append(tobs_dict)

    #Close session
    session.close()

    #Return JSON
    return jsonify(total_tobs)


#5. 
#- Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#- For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#- For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query
    start_data = session.query(func.min(measurement.tobs),func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    total_temp = []
    for min, max, avg in start_data
        temp_dict = {}
        temp_dict['min'] = min
        temp_dict['max'] = max
        temp_dict['avg'] = avg
        total_temp.append(temp_dict)

     #Close session
    session.close()

     #Return JSON
    return jsonify(total_temp)

@app.route("/api/v1.0/<start>/<end>")
def startend ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query
    end_data = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    total_end = []
    for min, max, avg in end_data:
        end_dict = {}
        end_dict['min'] = min
        end_dict['max'] = max
        end_dict['avg'] = avg
        total_end.append(end_dict)
    
    #Close session
    session.close()

    #Return JSON
    return jsonify(total_end)

if __name__ == "__main__":
    app.run(debug=True)
    








