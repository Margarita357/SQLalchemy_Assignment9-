from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct, desc, and_

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
session = Session(engine)
Measurement = Base.classes.measurement	
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
	return("Hello! If entering date, please enter in the format: YYYY-MM-DD")

@app.route('/api/v1.0/precipitation')
def precipitation(): 
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
	date = dt.datetime.strptime(last_date, "%Y-%m-%d")
	date2 = date - dt.timedelta(days = 365)
	date3 = date2.strftime( "%Y-%m-%d")

	prcp_dates = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date3).all()
	prcp = []
	for row in prcp_dates:
		prcp_dict = {}
		prcp_dict['date'] = row[0]
		prcp_dict['precipitation']	= row[1]
		prcp.append(prcp_dict)
	return jsonify(prcp)


@app.route("/api/v1.0/stations")
def station():
	
	stations = session.query(distinct(Measurement.station)).all()
	print(len(stations))
	station = []
	for row in stations:
		station_dict = {}
		station_dict['station']= row[0]
		station.append(station_dict)

	return jsonify(station)


@app.route("/api/v1.0/tobs")
def tobs():
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
	date = dt.datetime.strptime(last_date, "%Y-%m-%d")
	date2 = date - dt.timedelta(days = 365)
	date3 = date2.strftime( "%Y-%m-%d")

	tobs_dates = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > date3).all()
	tobs = []
	for row in tobs_dates:
		tobs_dict = {}
		tobs_dict['date'] = row[0]
		tobs_dict['tobs']	= row[1]
		tobs.append(tobs_dict)
	return jsonify(tobs)

#start date 
@app.route("/api/v1.0/<start>")
def calc(start):
	cononicalized = start.replace("/", "-")
	calc_temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(and_(Measurement.date>=cononicalized)).all()
	calc = []
	for row in calc_temp:
		calc_dict = {}
		calc_dict['min_tobs'] = row[0]
		calc_dict['max_tobs'] = row[1]
		calc_dict['ave_tobs'] = row[2]
		calc.append(calc_dict)

	return jsonify(calc)

@app.route("/api/v1.0/<start>/<end>")
def calc2(start, end):
	start_date = start.replace("/", "-")
	end_date = end.replace("/", "-")
	calc_temp2 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(and_(Measurement.date>=start_date, Measurement.date<=end_date)).all()
	calc2 = []
	for row in calc_temp2:
		calc_dict2 = {}
		calc_dict2['min_tobs'] = row[0]
		calc_dict2['max_tobs'] = row[1]
		calc_dict2['ave_tobs'] = row[2]
		calc2.append(calc_dict2)
	return jsonify(calc2)	

if __name__ == "__main__":
	app.run(debug=False)

#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404



# * Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.

# * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
#   for all dates greater than and equal to the start date.

# * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#   for dates between the start and end date inclusive.







 


