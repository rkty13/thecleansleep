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

@app.route('/rate')
def rate():
	return 'rate here!'