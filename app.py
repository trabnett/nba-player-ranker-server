from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
import json
import os
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials


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
            subscription_key = "a4c5ea3ef0fa4ab38a4d0cd61cb2f41e"
            search_term = name
            client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))
            client2 = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
            web_data = client.web.search(query=name)
            image_results = client2.images.search(query=search_term)
            class Object:
                def toJSON(self):
                    return json.dumps(self, default=lambda o: o.__dict__, 
                        sort_keys=True, indent=4)
            res = Object()
            res.image = image_results.value
            res.data = web_data
            # db.session.add(highscore)
            # db.session.commit()
            x = res.data.additional_properties['entities']['value'][0]['description']
            if ("nba" in x.lower()) or ("national basketball association" in x.lower()):
                payload = {"data": x}
            else:
                payload = {"alert": "Hmmm. Are you sure that is an NBA player?"}

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

