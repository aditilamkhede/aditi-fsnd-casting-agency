import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def index():
      result = "Coming Soon!!"
      return result

  @app.route('/movies')
  def get_movies():
      movies = "Check out incoming Movies Soon!!"
      return movies

  @app.route('/actors')
  def get_actors_all():
      actors = "Check it Out!!"
      return actors

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
