from flask import Flask, render_template, request, session, redirect, jsonify
import jinja2
import os
import hashlib
import json
from bson.objectid import ObjectId

import datetime
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

MONGO_URL = os.environ.get('MONGOLAB_URI')
client = MongoClient(MONGO_URL)
db = client.heroku_app30619679
collection = db.hotels
url = "cleansleep.herokuapp.com"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/rate', methods=['GET', 'POST'])
def rate():
	if request.method == 'POST':
		rating = request.form['rating']
		hotel_name = request.form['pac_input']
		name = request.form['name']
		comment = request.form['comment']
		lat = request.form['latitude']
		lng = request.form['longitude']


		collection.update( { "name" : hotel_name } , { "$push" : {"ratings" : rating }}, upsert=True)
		collection.update( { "name" : hotel_name }, { "$push" : {"comments" : {"name" : name, "comment" : comment, "rating" : rating}}}, upsert=True)
		collection.update({"name":hotel_name},{"$set":{"lat":lat,"lng":lng}})
		return redirect('/rate')

	hotels = []

	for record in collection.find():
		ratings = record['ratings']
		total = 0.0
		counter = 0.0
 		
		for x in range(0, len(ratings)):
			total += float(str(ratings[x]))
			counter += 1.0

		average = total/counter
		hotels.append({ "name" : record['name'], "rating" : round(average, 2), "url" : str(record['_id']) })

	return render_template('rate.html', hotels=hotels)

@app.route('/list', methods=['GET'])
def list():
	hotels = []

	for record in collection.find():
		ratings = record['ratings']
		total = 0.0
		counter = 0.0
			
		for x in range(0, len(ratings)):
			total += float(str(ratings[x]))
			counter += 1.0

		average = total/counter
		hotels.append({ "_id" : str(record['_id']), "name" : record['name'], "rating" : round(average, 2), "url" : str(record['_id']), "lat" : record['lat'], "lng" : record['lng'] })

	return jsonify(hotels=hotels)

@app.route('/browse')
def browse():
	hotels = []

	for record in collection.find():
		ratings = record['ratings']
		total = 0.0
		counter = 0.0
 		
		for x in range(0, len(ratings)):
			total += float(str(ratings[x]))
			counter += 1.0

		average = total/counter
		hotels.append({ "_id" : str(record['_id']) , "name" : record['name'], "rating" : round(average, 2), "url" : str(record['_id']) })
	return render_template('browse.html', hotels=hotels)

@app.route('/browse/<hotel_id>')
def hotels(hotel_id):
	record = collection.find_one({"_id": ObjectId(hotel_id)})

	comments = []
	comments_db = record["comments"]
	for x in range(0, len(comments_db)):
		comments.append(comments_db[x])

	hotel = []
	ratings = record["ratings"]
	total = 0.0
	counter = 0.0

	for x in range(0, len(ratings)):
		total += float(str(ratings[x]))
		counter += 1.0

	average = total/counter
	hotel.append({"name" : record["name"], "rating" : round(average, 2)})
	return render_template('hotels.html', hotel=hotel[0],comments=comments)

@app.route('/about')
def about():
	return render_template('about.html')
