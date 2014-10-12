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

<<<<<<< HEAD
	hotels = {}

	h_counter = 0

	for record in collection.find():
		ratings = record['ratings']
		total = 0
		counter = 0
 		
		for x in range(0, len(ratings)):
			total += ratings[x]
			counter += 1
		hotels[h_counter] = { "name" : record['name'], "rating" : total/counter}

		h_counter += 1


	return render_template('rate.html', hotels=hotels)
=======
	return render_template('rate.html')

@app.route('/about')
def about():
	return render_template('about.html')
>>>>>>> 19d80e1325fe479b15807e00740836669bd2c3e7
