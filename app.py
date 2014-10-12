from flask import Flask, render_template, request, session, redirect, jsonify
import jinja2
import os
import hashlib

import datetime
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

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

		collection.update( { "name" : hotel_name }, { "$push" : {"ratings" : { "rating": rating }}}, upsert=True)

		return redirect('/rate')

	return render_template('rate.html')

@app.route('/about')
def about():
	return render_template('about.html')