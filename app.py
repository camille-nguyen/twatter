from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

client = pymongo.MongoClient("mongodb+srv://camille:pavina88@twatter.oexcf.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/signup')
  
  return wrap

from user import routes

@app.route('/signup')
def home():
    return render_template("home.html")

@app.route('/log')
def log():
    if 'logged_in' in session:
        return render_template("dashboard.html")
    else:
        return render_template("log.html")

@app.route('/')
@login_required
def dashboard():
  twat_collection = db.twats
  twats = twat_collection.find()
  return render_template('dashboard.html', twats=twats)

from user.routes import main
app.register_blueprint(main)