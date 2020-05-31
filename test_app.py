import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# from flaskr import create_app
from app import app
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the  test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_app()
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        print('casting_assistant', os.environ['auth_token_cast_asst'])
        # client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer your_token'
        # auth_header = { 'Authorization': 'Bearer {}'.format(os.environ['auth_token'])}
        # The access token is a string in the format of "Bearer ejyxhs..."
        self.casting_assistant = { 'Authorization': 'Bearer {}'.format(os.environ['auth_token_cast_asst'])}
        self.casting_director = { 'Authorization': 'Bearer {}'.format(os.environ['auth_token_cast_dir'])}
        self.executive_producer = { 'Authorization': 'Bearer {}'.format(os.environ['auth_token_exec_prod'])}

        self.new_movie = {
            'title': 'Movie1',
            'release_date': '05-22-2019'}

        self.update_movie = {
            'title': 'Movie2',
            'release_date': '05-22-2008'}

        self.new_actor = {
            'name': 'Actor1 F',
            'age': '25',
            'gender': 'Female'}

        self.update_actor = {
            'name': 'Actor2 M',
            'age': '28',
            'gender': 'Male'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        # self.db.drop_all()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_405_not_allowed(self):
        res = self.client().get('/movies/100', headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed, Please Check URL.')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_405_not_allowed(self):
        # res = self.client().get('/actors?page=1000')
        res = self.client().get('/actors/100', headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed, Please Check URL.')

    def test_create_movie_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie)
        # , headers=self.casting_assistant,json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], {'code': 'authorization_header_missing', 'description':'Authorization header is expected.'})
        # self.assertEqual(data['success'], False)

    def test_delete_movie_casting_assistant(self):
        res = self.client().delete('/movies/5')
        # , headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {'code': 'authorization_header_missing', 'description':'Authorization header is expected.'})

    def test_create_actor_casting_assistant(self):
        res = self.client().post('/actors', headers=self.casting_assistant,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], {
        'code': 'permissions_payload', 'description':'Payload does not contain "permissions" string.'})

    def test_delete_actor_casting_assistant(self):
        res = self.client().delete('/actors/10')
        # , headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {
        'code': 'authorization_header_missing', 'description':'Authorization header is expected.'})

    def test_create_movie_casting_director(self):
        res = self.client().post('/movies', headers=self.casting_director,
                json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {'code': 'permissions_payload', 'description':'Payload does not contain "permissions" string.'})

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/7')
        # , headers=self.casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {'code': 'authorization_header_missing', 'description':'Authorization header is expected.'})

    def test_update_movie_casting_director(self):
        res = self.client().patch('/movies/1', headers=self.casting_director,
                json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie_404_not_found_casting_director(self):
        res = self.client().patch('/movies/1000', headers=self.casting_director,
                json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Movie id not found.')

    def test_create_actor_casting_director(self):
        res = self.client().post('/actors', headers=self.casting_director,
                json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/19', headers=self.casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_404_not_found_casting_director(self):
        res = self.client().delete('/actors/1000', headers=self.casting_director)
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Actor id not found.')

    def test_update_actor_casting_director(self):
        res = self.client().patch('/actors/1', headers=self.casting_director,
                json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor_404_not_found_casting_director(self):
        res = self.client().patch('/actors/1000', headers=self.casting_director,
                json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Actor id not found.')

    def test_create_movie_executive_producer(self):
        res = self.client().post('/movies', headers=self.executive_producer,
                json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_executive_producer_405_not_allowed(self):
        res = self.client().post('/movies/100',headers=self.executive_producer,
                json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed, Please Check URL.')

    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/17', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_404_not_found_executive_producer(self):
        res = self.client().delete('/movies/1000', headers=self.executive_producer)
        data = json.loads(res.data)
        print('test_delete_movie_404_not_found_executive_producer', data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Movie id not found.')

    def test_update_movie_executive_producer(self):
        res = self.client().patch('/movies/1', headers=self.executive_producer,
                json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie_404_not_found_executive_producer(self):
        res = self.client().patch('/movies/1000', headers=self.executive_producer,
                json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False
        self.assertEqual(data['message'], 'Movie id not found.')

    def test_update_actor_executive_producer(self):
        res = self.client().patch('/actors/1', headers=self.executive_producer,
                json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor_404_not_found_executive_producer(self):
        res = self.client().patch('/actors/1000', headers=self.executive_producer,
                json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Actor id not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
