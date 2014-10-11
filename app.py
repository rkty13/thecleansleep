import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'Welcome to the clean sleep!'

@app.route('/rate')
def rate():
	return 'rate here!'