import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/rate')
def rate():
	return 'rate here!'