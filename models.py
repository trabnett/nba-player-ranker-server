from app import db
from datetime import datetime
import time

class Highscore(db.Model):
    __tablename__ = 'highscore'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    ppg = db.Column(db.Float())
    rebounds = db.Column(db.Float())
    assists = db.Column(db.Float())
    per = db.Column(db.Float())
    picture_url = db.Column(db.String())
    rating = db.Column(db.Integer())


    def __init__(self, name, ppg, rebounds, assists, per, picture_url, rating):
        self.name = name
        self.ppg = ppg
        self.rebounds = rebounds
        self.assists = assists
        self.per = per
        self.picture_url = picture_url
        self.rating = rating

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'ppg': self.ppg,
            'rebounds': self.rebounds,
            'assists': self.assists,
            'per': self.per,
            'picture_url': self.picture_url,
            'rating': self.rating
        }
    
class IP(db.Model):
    __tablename__ = 'IP'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(140))
    timestamp = db.Column(db.Integer, default=int(time.time()))
    count = db.Column(db.Integer)

def __repr__(self):
    return '<IP {}>'.format(self.body)