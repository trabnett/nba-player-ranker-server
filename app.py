from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from helpers import Playersonly
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
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
    check = Playersonly()
    check.name = name
    check.formatName()
    print(check.url)
    name = check.name
    quote_page = f'https://www.basketball-reference.com/players/{check.url[0]}/{check.url}01.html'
    print(quote_page)
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    career_stats = soup.find('div', attrs={'class': 'stats_pullout'})
    check.ppg = career_stats.find_all('p')[5].text
    check.rebounds = career_stats.find_all('p')[7].text
    check.assists = career_stats.find_all('p')[9].text
    check.per = career_stats.find_all('p')[19].text
    print(check.name, check.ppg, check.rebounds, check.assists, check.per)
    new_player = Highscore.query.filter_by(name=name).first()
    # if new_player is None:
    #     try:
    #         highscore=Highscore(
    #             name=name,
    #             total=total,
    #             date=date
    #         )
    #         subscription_key = os.environ['AZURE_KEY']
    #         search_term = name
    #         client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))
    #         client2 = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
    #         web_data = client.web.search(query=name)
    #         image_results = client2.images.search(query=search_term)
    #         class Object:
    #             def toJSON(self):
    #                 return json.dumps(self, default=lambda o: o.__dict__, 
    #                     sort_keys=True, indent=4)
    #         res = Object()
    #         check = Object()
    #         res.image = image_results.value
    #         check.data = web_data
    #         print(check.data.additional_properties)
            # db.session.add(highscore)
            # db.session.commit()
        #     x = check.data.additional_properties['entities']['value'][0]['description']
        #     y = res.image[0].content_url
        #     if ("nba" in x.lower()) or ("national basketball association" in x.lower()):
        #         payload = res.toJSON()
        #     else:
        #         payload = {"alert": "Hmmm. Are you sure that is an NBA player?"}

        #     print(x)
        #     print(y)
        #     return jsonify(payload)
        # except Exception as e:
        #     return(str(e))
    # else:
    #     error = {'error': 'that player is already registered'}
    #     return jsonify(error)

@app.route("/getall")
def get_all():
    try:
        highscores=Highscore.query.all()
        return  jsonify([e.serialize() for e in highscores])
    except Exception as e:
	    return(str(e))

