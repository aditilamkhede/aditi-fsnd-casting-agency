import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "castingAgency"
database_path = os.environ['DATABASE_URL']
# "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)
    db.create_all()

mov_act_rel_table = db.Table('mov_act_rel_table',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.PrimaryKeyConstraint('movie_id', 'actor_id')
)

class Movies(db.Model):
    """docstring for Movies."""
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    release_date = Column(db.DateTime)
    actors = db.relationship('Actors', secondary='mov_act_rel_table',
        backref=db.backref('movies', lazy=True))


    def __init__(self, arg):
        super(Movies, self).__init__()
        self.arg = arg

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
        }

class Actors(db.Model):
    """docstring for Actors."""
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(String(20))

    def __init__(self, arg):
        super(Actors, self).__init__()
        self.arg = arg

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }
