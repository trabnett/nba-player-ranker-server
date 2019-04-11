from app import db

class Highscore(db.Model):
    __tablename__ = 'highscore'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    total = db.Column(db.Integer)
    date = db.Column(db.Date())

    def __init__(self, name, total, date):
        self.name = name
        self.total = total
        self.date = date

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'total': self.total,
            'date':self.date
        }