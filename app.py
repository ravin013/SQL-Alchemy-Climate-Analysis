from flask import Flask,jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    """List of all available API routes"""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")

def precipitation():
    """Query for precipitation date for last year"""
    
    precipitationdatalastyear = session.query(Measurement.prcp,Measurement.date).\
    filter(Measurement.date > '2016-08-22').all()

    all_prcp = list(np.ravel(precipitationdatalastyear))
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of stations from the dataset in JSON format"""
    
    station_results = session.query(Station.station).all()
    
    # Convert the list of tuples into a normal list:
    allstations = list(np.ravel(station_results))
    
    return jsonify(allstations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a list of temperature observations from the last year in JSON format"""
    
    tobs_results = session.query(Measurement.tobs).\
    filter(Measurement.date > '2016-08-22').all()
    
    # Convert the list of tuples into normal list:
    alltobs = list(np.ravel(tobs_results))
    
    return jsonify(alltobs)

@app.route("/api/v1.0/start")
def start():
    """Returns the average, max, and min temperature for a given start date"""
    
    averages = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= '2016-08-22').filter(Measurement.date <= '2017-08-22').all()
    
    averages = list(np.ravel(averages))
    
    return jsonify(averages)


@app.route("/api/v1.0/start/end")
def startend():
    """Returns the average, max, and min temperature between two dates"""
    allaverages = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= '2016-08-22')
    
    allaverages = list(np.ravel(allaverages))
    
    return jsonify(allaverages)

if __name__ == "__main__":
    app.run(debug=True)
