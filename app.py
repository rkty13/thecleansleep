from flask import Flask, render_template, request, session, redirect, jsonify
import jinja2
import os
import hashlib
import json

import datetime
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

MONGO_URL = os.environ.get('MONGOLAB_URI')
client = MongoClient(MONGO_URL)
db = client.heroku_app30619679
collection = db.hotels

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/rate', methods=['GET', 'POST'])
def rate():
	if request.method == 'POST':
		rating = request.form['rating']
		hotel_name = request.form['pac_input']

		collection.update( { "name" : hotel_name }, { "$push" : {"ratings" : rating }}, upsert=True)

		return redirect('/rate')

	hotels = []

	h_counter = 0

	for record in collection.find():
		ratings = record['ratings']
		total = 0.0
		counter = 0.0
 		
		for x in range(0, len(ratings)):
			total += float(str(ratings[x]))
			counter += 1.0

		average = total/counter
		print(average)
		hotels.append({ "name" : record['name'], "rating" : round(average, 2) })

		h_counter += 1

	return render_template('rate.html', hotels=hotels)

@app.route('/browse')
def browse():
	hotels = {}

	h_counter = 0

	for record in collection.find():
		ratings = record['ratings']
		total = 0
		counter = 0
 		
		for x in range(0, len(ratings)):
			total += int(ratings[x])
			counter += 1
		hotels[h_counter] = { "name" : record['name'], "rating" : str(total/counter)}

		h_counter += 1


	return render_template('browse.html', hotels=hotels)

@app.route('/about')
def about():
	return render_template('about.html')
