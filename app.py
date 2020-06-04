import os
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth, no_cache

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
import http.client
import datetime

DATA_PER_PAGE = 10
YOUR_CLIENT_SECRET = "-Cvi9-nsnz7vOMnv9OApmF4Twd1a7afTiXo2I42Zrl4WwO_clj6cbDRdH7Q9_guY"
YOUR_CALLBACK_URL = "http://localhost:5000/callback"
SECRET_KEY = "aditicapstonendsecret"
AUTH0_AUTHORIZE_URL = "https://udacity-nd-capstone.auth0.com/authorize?audience=casting&response_type=token&client_id=9EalhHTVUmqwMnnF94DT00JuoIHkYtcx&redirect_uri=http://127.0.0.1:5000/callback"

database_path = os.environ['DATABASE_URL']

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_db(app, database_path)
    CORS(app, expose_headers='Authorization')

    # oauth = OAuth(app)
    #
    # auth0 = oauth.register(
    #     'auth0',
    #     client_id='9EalhHTVUmqwMnnF94DT00JuoIHkYtcx',
    #     client_secret=YOUR_CLIENT_SECRET,
    #     api_base_url='https://udacity-nd-capstone.auth0.com',
    #     access_token_url='https://udacity-nd-capstone.auth0.com/oauth/token',
    #     authorize_url='https://udacity-nd-capstone.auth0.com/authorize',
    #     client_kwargs={
    #         'scope': 'openid profile email',
    #     },
    # )

    @app.after_request
    def after_request(response):
        print('In after_request')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS')
        # if session.get('jwt_token'):
        #     # print('Found it.....', request.headers)
        #     response.headers.add('Authorization', 'Bearer '+ str(session['jwt_token']))
        # print(response.headers)
        return response

    @app.before_request
    def before_request():
        print('In before_request', datetime.datetime.now())
        # print(request.headers)
        # get_token_header()
        # test="dhjdhjsa"

    @app.route('/login')
    def login():
        print('In login')
        return auth0.authorize_redirect(redirect_uri=YOUR_CALLBACK_URL, audience='casting')


    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {'returnTo': url_for('dashboard', _external=True), 'client_id': '9EalhHTVUmqwMnnF94DT00JuoIHkYtcx'}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


    @app.route('/callback')
    def callback_handling():
        print('In callback handling')
        jwt_token = ""
        try:
            # Handles response from token endpoint
            # print(auth0)
            # token = auth0.authorize_access_token()
            # jwt_token = token['id_token']
            # print(jwt_token)

            session['jwt_token'] = jwt_token

            # resp = auth0.get('userinfo')
            # userinfo = resp.json()
            # # print('Before session', userinfo)
            # # Store the user information in flask session.
            # session['jwt_payload'] = userinfo
            # # print('after session', session)
            # session['profile'] = {
            #     'user_id': userinfo['sub'],
            #     'name': userinfo['name'],
            #     'picture': userinfo['picture']
            # }
        except Exception as e:
            print('exception',e)

        return redirect('/')
        # response = make_response(redirect('/dashboard'))
        # response.headers['Authorization'] = 'Bearer '+ jwt_token
        # response.set_cookie('jwt_token', 'Bearer '+ jwt_token)
        # return response


    @app.route('/dashboard')
    # @requires_auth()
    def dashboard():
        # return render_template('dashboard.html',
        #            userinfo=session['profile'],
        #            userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
        print('request.args', request.args)
        token = request.args.get('access_token', default = '', type = str)
        print('token', token)
        session['jwt_token'] = token
        response = make_response(render_template('dashboard.html'))
        # response.headers.set('Authorization', 'Bearer '+ str(session['jwt_token']))
        response.set_cookie('jwt_token', token)
        return response

    @app.route('/')
    # @cross_origin
    def index():
        token = request.args.get('access_token', default = '', type = str)
        print('Index token', token)
        session['jwt_token'] = token
        result = "Coming Soon!!"
        # print("request.headers in Index - ", request.headers)
        # return render_template('index.html'   )
        response = make_response(render_template('index.html'))
        # response.headers.set('Authorization', 'Bearer '+ str(session['jwt_payload']))
        response.set_cookie('jwt_token', token)
        return response


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

    @app.route('/getcookie')
    def get_token_header():
        # print('request.cookies', request.cookies)
        token = request.cookies.get('jwt_token')
        print('get_token_header token', token)
        conn = http.client.HTTPSConnection("localhost", 5000)

        headers = {
            # 'content-type': "application/json",
            'Authorization': "Bearer "+token
            }

        conn.request("GET", "/movies", headers=headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))


    # Movies end points
    # end point to list all movies
    @app.route('/movies')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('get:lists')
    def get_movies(payload):
        data = {}
        try:
            print('In Movies1')
            movies = Movies.query.all()
            movs = paginate_data(request, movies, True)

            if (len(movs) == 0):
                 raise AuthError('Movies not found.', status_code=404)
            # return jsonify({
            #     'success': False})
            data = jsonify({
                'success': True,
                'movies': movs,
                'total_movies': len(movies)
                })
            print('Movies data', movs)
        except Exception as e:
            print('error in movies')
            raise

        # return render_template('movies.html', results=movs)
        return data
        # return jsonify({'data': render_template('movies.html', results=movs)})


    # end point to add movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def movies_create(payload):
        try:
            print('Inside check Json')
            body = request.get_json()
            # print('body',request.get_json())

            new_title = body.get('title', None)
            new_relDate = body.get('release_date', None)
            print(new_title)
            movie = Movies(title=new_title, release_date=new_relDate)
            movie.insert()
        except Exception as e:
            print('In Add Movie', e)
            raise AuthError('Error in Create Movie.', status_code=404)

        return jsonify({'success' : True,
                        'new id': movie.id})

    # end point to delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def movies_delete(payload, movie_id):
        try:
            movie = Movies.query.filter(Movies.id==movie_id).one_or_none()
            if movie is None:
                raise AuthError('Movie id not found.', status_code=404)
            movie.delete()
        except Exception as e:
            print('In Movie Delete Error')
            raise

        return jsonify({'success': True})

    # end point to update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:item')
    def movies_update(payload, movie_id):
        try:
            body = request.get_json()

            req_title = body.get('title', None)
            req_relDate = body.get('release_date', None)

            movie = Movies.query.filter(Movies.id==movie_id).one_or_none()
            if movie is None:
                raise AuthError('Movie id not found.', status_code=404)

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
    @requires_auth('get:lists')
    def get_actors_all(payload):
        # actors = "Check it Out!!"
        # return actors
        try:
            actors = Actors.query.all()
            acts = paginate_data(request, actors, False)

            if (len(acts) == 0):
              raise AuthError('Error in actors list.', status_code=404)
              # return jsonify({
              #     'success': False})
        except Exception as e:
            print('error in actors', e)
            raise

        data = jsonify({
            'success': True,
            'actors': acts,
            'total_actors': len(actors)
        })
        print('actors list', acts)

        # return render_template('actors.html', results=acts)
        return data

    # end point to add actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def actors_create(payload):
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

        return jsonify({'success' : True,
                        'new id': actor.id})

    # end point to delete a actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def actors_delete(payload, actor_id):
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
    @requires_auth('update:item')
    def actors_update(payload, actor_id):
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
            'updateActor': {'id':actor.id,
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

    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Authorization header is expected.'
            }), 401

    @app.errorhandler(403)
    def permission_error(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Payload does not contain "permissions" string.'
            }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found.'
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
