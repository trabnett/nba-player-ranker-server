from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
import os


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Highscore


@app.route("/")
def welcome():
    return "Welcome to the nba highscore app server!"

@app.route("/add")
def add_event():
    name=request.args.get('name')
    total=request.args.get('total')
    date=request.args.get('date')
    new_player = Highscore.query.filter_by(name=name).first()
    if new_player is None:
        try:
            highscore=Highscore(
                name=name,
                total=total,
                date=date
            )
            db.session.add(highscore)
            db.session.commit()
            payload = {'highscore_id': highscore.id}
            return jsonify(payload)
        except Exception as e:
            return(str(e))
    else:
        error = {'error': 'that player is already registered'}
        return jsonify(error)

@app.route("/getall")
def get_all():
    try:
        highscores=Highscore.query.all()
        return  jsonify([e.serialize() for e in highscores])
    except Exception as e:
	    return(str(e))

