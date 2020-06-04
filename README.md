# CASTING AGENCY

CASTING AGENCY models a company that is responsible for creating movies and managing and assigning actors to those movies.
Thus app was created to simplify and streamline process.

This application allows to add new movies and actors, get list of all movies and actors. Update and delete a movie and  an actor.

This project is the Capstone project for FULL STACK NANODEGREE PROGRAM at UDACITY. I wanted to implement a fully working casting agency website including front end where I will be able to implement or use most of the technical skills I learned in this program.

At this point FrontEnd is not complete. Though I am planning to implement it soon.

## Getting Started

We have created a REST API CASTING AGENCY.
This API is implemented using following:

 - Python3, Flask
 - SQLAlchemy ORM
 - PostgreSQL Database

## Pre-requisites

Python3, pip should be installed on local machine.

### Backend

From the backend folder run requirements.txt.

pip install -r requirements.txt

#### Database Setup
Restore a database using the castingAgency.psql file provided.
From the backend folder in terminal run:

psql castingAgency < castingAgency.psql

To run the application, execute:

First setup the environment variable by running following command:
. setup_test.sh

export FLASK_APP=app.py
export FLASK_ENV=development
flask run

### Frontend

Frontend is not complete yet. You can login using the login menu. Other menu options are just placeholders.

## Testing
To run the tests navigate to backend folder and run the following commands:

dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python3 test_app.py

If you are running the commands first time, exclude dropdb command.

All tests are included in the test_app.py and should be maintained as updates are made to the application.

## API Reference

### Getting Started

    1. Base URL: Application is hosted on Heroku. Application also runs locally. Application is hosted at

    https://aditi-fsnd-casting-agency.herokuapp.com/.
    
    2. Authentication: Application uses auth0 API for authentication.

      Application has three roles with their respective RBAC:
      * Casting Assistant
        * Can view actors and movies
      * Casting Director
          * All permissions a Casting Assistant has and…
          * Add or delete an actor from the database
          * Modify actors or movies
      * Executive Producer
        * All permissions a Casting Director has and…
        * Add or delete a movie from the database

      To test the end points using curl command. First run the setup.sh file to setup the environment variables and then run curl command using setup.sh variables for different RBAC.

      $ . setup.sh
      setup.sh has tokens for all 3 roles.

      To get list of actors using casting assistant role, run following curl command after running above setup.sh

      curl -H "Authorization: Bearer ${auth_token_cast_asst}" https://aditi-fsnd-casting-agency.herokuapp.com/actors


### Error Handling

  Errors are returned as json objects:
    {
      'success': False
      'error': 422,
      'message': 'Request is not processable.'
    }

  Application returns following error codes:

  - 200 - OK(success)

  - 400 - Bad Request

  - 401 - Authorization header is expected

  - 403 - Payload does not contain "permissions" string.

  - 404 - Resource Not Found

  - 405 - Method not allowed

  - 422 - Not processable

  - 500 - Internal Server Error

### End Points

Application has following end points. Example curl url with jwt token is mentioned below for reference. However replace those token values with current auth0 token or run setup.sh as mentioned in "Authentication" part of section [Link to Header](#getting-started).

    - GET
      - /movies
      - /actors
    - POST
      - /movies/{movie_id}
      - /actors/{actor_id}
    - DELETE
      - /movies/{movie_id}
      - /actors/{actor_id}
    - PATCH
      - /movies/{movie_id}
      - /actors/{actor_id}

#### End Points in Detail

##### GET /movies

    1. Returns a list of movies, total movies and success value.

###### Sample

      curl -H "Authorization: Bearer ${auth_token_cast_asst}" https://aditi-fsnd-casting-agency.herokuapp.com/movies

      {
        "movies":
          [
            {
              "id":1,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":2,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":3,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie2"
            },
            {
              "id":4,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":5,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {{
              "id":6,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":7,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":8,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            }
          ],
        "success":true,
        "total_movies":8
      }

##### DELETE /movies/{movie_id}

      1. Deletes a movie of the given id.
      2. Returns the success value.

###### Sample

      curl -H "Authorization: Bearer ${auth_token_cast_asst}" -X DELETE https://aditi-fsnd-casting-agency.herokuapp.com/movies/5

        {
          "success": true
        }

##### POST /movies

      1. Adds a new movie to the movies list.
      2. Returns a newly created Id and success value.

###### Sample

      curl -d '{"title":"Movie1", "release_date":"05-22-2019"}'
      -H "Content-Type: application/json"
      -H "Authorization: Bearer ${auth_token_cast_asst}"
      -X POST https://aditi-fsnd-casting-agency.herokuapp.com/movies

      {
        "new id":8,
        "success":true
      }

##### PATCH /movies/{movie_id}

      1. Updates a movie data based on given id.
      2. Returns success value.

###### Sample
      curl -d '{"title":"Movie2", "release_date":"02/22/2017"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${auth_token_cast_asst}" -X PATCH https://aditi-fsnd-casting-agency.herokuapp.com/movies/2

      {
        "success":true
      }

##### GET /actors

    1. Returns a list of actors, success value and total actors.
    <!-- 2. Results are also paginated. -->

###### Sample:
      curl -H "Authorization: Bearer ${auth_token_cast_asst}" https://aditi-fsnd-casting-agency.herokuapp.com/actors

      {
        "actors":
          [
            {
              "age":24,
              "gender":"F",
              "id":1,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":2,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":3,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":4,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":5,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":6,
              "name":"Actor 1"
            }
          ],
        "success":true,
        "total_actors":6
      }


##### POST /actors

      1. Adds a new actor to the actors list.
      2. Returns a newly created Id and a success value.

###### Sample
         curl -d '{"name":"Actor 1", "age":"24", "gender":"F"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${auth_token_cast_asst}" -X POST https://aditi-fsnd-casting-agency.herokuapp.com/actors

        {
          "new id":9,
          "success":true
        }

##### DELETE /actors/{actor_id}

      1. Deletes an actor of the given id.
      2. Returns the success value.

###### Sample

      curl -H "Authorization: Bearer ${auth_token_cast_asst}" -X DELETE https://aditi-fsnd-casting-agency.herokuapp.com/actors/5

      {
        "success": true
      }

##### PATCH /actors/{actor_id}

      1. Updates an actors data based on given id.
      2. Returns updated actor information and success value.

###### Sample
        curl -d '{"name":"Actor 1 F", "age":"24", "gender":"F"}'
        -H "Content-Type: application/json"
        -H "Authorization: Bearer ${auth_token_cast_asst}"
        -X PATCH https://aditi-fsnd-casting-agency.herokuapp.com/actors/2

          {
            "updateActor":
            {
              "age":24,
              "gender":"F",
              "id":2,
              "name":"Actor 1 F"
            },
            "success":true
          }
