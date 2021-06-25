from flask.json import jsonify
from .shareddb import db
from flask import jsonify


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50))  
    password = db.Column(db.String(50))

    def __init__(self, name:str, username:str, password:str, id=None):
        self.name = name
        self.username = username
        self.password = password
        if id: self.id = id
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
        }
