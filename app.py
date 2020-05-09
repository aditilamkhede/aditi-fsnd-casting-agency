import os
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

# from dotenv import load_dotenv, find_dotenv
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

DATA_PER_PAGE = 10
YOUR_CLIENT_SECRET = "-Cvi9-nsnz7vOMnv9OApmF4Twd1a7afTiXo2I42Zrl4WwO_clj6cbDRdH7Q9_guY"
YOUR_CALLBACK_URL = "http://localhost:5000/callback"
SECRET_KEY = "aditicapstonendsecret"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_db(app)
    CORS(app)

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id='9EalhHTVUmqwMnnF94DT00JuoIHkYtcx',
        client_secret=YOUR_CLIENT_SECRET,
        api_base_url='https://udacity-nd-capstone.auth0.com',
        access_token_url='https://udacity-nd-capstone.auth0.com/oauth/token',
        authorize_url='https://udacity-nd-capstone.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    @app.after_request
    def after_request(response):
        print('In after_request')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS')
        if session.get('jwt_token'):
            print('Found it.....', request.headers)
            response.headers.add('Authorization', 'Bearer '+ str(session['jwt_token']))
        print(response.headers)
        return response

    @app.route('/login')
    def login():
        print('In login')
        return auth0.authorize_redirect(redirect_uri=YOUR_CALLBACK_URL)


    @app.route('/callback')
    def callback_handling():
        print('In callback handling')
        jwt_token = ""
        try:
            # Handles response from token endpoint
            print(auth0)
            token = auth0.authorize_access_token()
            jwt_token = token['id_token']
            print(jwt_token)
            # jwt_token = auth0.authorize_access_token()[‘id_token’]
            # print('Is Error')
            session['jwt_token'] = jwt_token

            resp = auth0.get('userinfo')
            userinfo = resp.json()
            # print('Before session', userinfo)
            # Store the user information in flask session.
            session['jwt_payload'] = userinfo
            # print('after session', session)
            session['profile'] = {
                'user_id': userinfo['sub'],
                'name': userinfo['name'],
                'picture': userinfo['picture']
            }
        except Exception as e:
            print('exception',e)

        # return redirect('/')
        response = make_response(redirect('/'))
        response.headers['Authorization'] = 'Bearer '+ jwt_token
        response.set_cookie('jwt_token', 'Bearer '+ jwt_token)
        # response.headers.set('Authorization', 'Bearer '+ str(session['jwt_payload']))
        # print('session - ', str(session['jwt_payload']))
        return response


    @app.route('/')
    def index():
        # token = request.args.get('access_token', default = '', type = str)
        # print('token', token)
        result = "Coming Soon!!"
        print("request.headers in Index - ", request.headers)
        return render_template('index.html'   )
        # response = make_response(render_template('index.html'))
        # response.headers.set('Authorization', 'Bearer '+ str(session['jwt_payload']))
        # return response


    def paginate_data(request, selection, isMovie):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * DATA_PER_PAGE
        end = start + DATA_PER_PAGE
        current_data = []

        if isMovie :
          movies = [Movies.format() for Movies in selection]
          current_data = movies[start:end]
        else:
          actors = [Actors.format() for Actors in selection]
          current_data = actors[start:end]

        return current_data


    # Movies end points
    # end point to list all movies
    @app.route('/movies')
    # @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('get:lists')
    def get_movies(payload):
        try:
            print('In Movies')
            movies = Movies.query.all()
            movs = paginate_data(request, movies, True)

            if (len(movs) == 0):
                 raise AuthError('Movies not found.', status_code=404)
            # return jsonify({
            #     'success': False})
        except Exception as e:
            print('error in movies')
            raise

        return jsonify({
            'success': True,
            'movies': movs,
            'total_movies': len(movies)
            })

    # end point to add movie
    @app.route('/movies', methods=['POST'])
    def movies_create():
        try:
            print('Inside')
            body = request.get_json()

            new_title = body.get('title', None)
            new_relDate = body.get('release_date', None)
            print(new_title)
            movie = Movies(title=new_title, release_date=new_relDate)
            movie.insert()
        except Exception as e:
            print('In Add Movie', e)
            raise AuthError('Movie id not found.', status_code=404)

        return jsonify({'success' : True})

    # end point to delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def movies_delete(movie_id):
        try:
            movie = Movies.query.filter(Movies.id==movie_id).one_or_none()
            if movie is None:
                raise AuthError('Actor id not found.', status_code=404)
            movie.delete()
        except Exception as e:
            print('In Movie Delete Error')
            raise

        return jsonify({'success': True})

    # end point to update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def movies_update(movie_id):
        try:
            body = request.get_json()

            req_title = body.get('title', None)
            req_relDate = body.get('release_date', None)

            movie = Movies.query.filter(Movies.id==movie_id).one_or_none()
            if movie is None:
                raise AuthError('Actor id not found.', status_code=404)

            if req_title:
                movie.title = req_title
            if req_relDate:
                movie.release_date = req_relDate

            movie.update()

        except Exception as e:
            print('In Movie Delete Error')
            raise

        return jsonify({'success': True})

    # Actors end points
    # end point to get list of actors
    @app.route('/actors')
    def get_actors_all():
        # actors = "Check it Out!!"
        # return actors
        try:
            actors = Actors.query.all()
            acts = paginate_data(request, actors, False)

            if (len(acts) == 0):
              raise AuthError('Actor id not found.', status_code=404)
              # return jsonify({
              #     'success': False})
        except Exception as e:
            print('error in actors', e)
            raise

        return jsonify({
            'success': True,
            'actors': acts,
            'total_actors': len(actors)
        })

    # end point to add actors
    @app.route('/actors', methods=['POST'])
    def actors_create():
        try:
            body = request.get_json()
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            actor.insert()
        except Exception as e:
            print('In Add Actor', e)
            raise AuthError('Actor id not found.', status_code=404)

        return jsonify({'success' : True})

    # end point to delete a actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def actors_delete(actor_id):
        try:
            actor = Actors.query.filter(Actors.id==actor_id).one_or_none()
            if actor is None:
                print('Error in before raising exception')
                raise AuthError('Actor id not found.', status_code=404)
                # abort(404)
            actor.delete()
        except Exception as e:
            print('In Actor Delete Error', e)
            raise

        return jsonify({'success': True})

    # end point to modify a actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def actors_update(actor_id):
        try:
            body = request.get_json()
            req_name = body.get('name', None)
            req_age = body.get('age', None)
            req_gender = body.get('gender', None)

            actor = Actors.query.filter(Actors.id==actor_id).one_or_none()

            if actor is None:
                raise AuthError('Actor id not found.', status_code=404)

            if req_name:
                actor.name = req_name
            if req_age:
                actor.age = req_age
            if req_gender:
                actor.gender = req_gender

            actor.update()

        except Exception as e:
            print('In Actor Delete Error')
            raise
            # abort(422)

        return jsonify({
            'success': True,
            'newActor': {'id':actor.id,
                         'name':actor.name,
                         'age':actor.age,
                         'gender': actor.gender
                         }
            })

    # '''
    # Create error handlers for all expected errors
    # including 404 and 422.
    # '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'It is a Bad Request'
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
            }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed, Please Check URL.'
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request is not processable.'
            }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error. Server encountered an error.'
            }), 500

    # error handler for AuthError
    #     error handler should conform to general task above
    # '''
    @app.errorhandler(AuthError)
    def auth_error(error):
        # return jsonify({
        #     'success': False,
        #     'error': error.status_code,
        #     'message': error.to_dict()
        # })
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
