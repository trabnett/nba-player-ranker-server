from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from helpers import Playersonly, Object
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from requests import get
from bs4 import BeautifulSoup
import urllib.request
import socket
import json
import os
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from azure.cognitiveservices.search.videosearch import VideoSearchAPI
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
from datetime import datetime
import time


app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
subscription_key = os.environ['AZURE_KEY']

from models import Highscore, IP

@app.route("/")
def welcome():
    return "Welcome to the nba highscore app server!"

@app.route("/add")
def add_event():
    check = Playersonly()
    check.name = request.args.get('name')
    check.formatName()
    name = check.name
    new_player = Highscore.query.filter_by(name = name).first()
    if new_player is None:
        try:
            client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))
            web_data = client.web.search(query=name)
            x = web_data.additional_properties['entities']['value'][0]['description']
            if ("nba" in x.lower()) or ("national basketball association" in x.lower()) or ("retired" in x.lower()):
                quote_page = f'https://www.basketball-reference.com/players/{check.url[0]}/{check.url}01.html'
                page = urllib2.urlopen(quote_page)
                soup = BeautifulSoup(page, 'html.parser')
                career_stats = soup.find('div', attrs={'class': 'stats_pullout'})
                if career_stats is None:
                    payload = {'error': 'There is no basketball reference page for that player. Is it possible that you made a spelling mistake or are using a nickname? For instance, if you want Metta World Peace, search for Ron Artest'}
                    return jsonify(payload)
                else:
                    check.ppg = career_stats.find_all('p')[5].text
                    check.rebounds = career_stats.find_all('p')[7].text
                    check.assists = career_stats.find_all('p')[9].text
                    check.per = career_stats.find_all('p')[19].text
                    highscore = Highscore(
                        name = name,
                        ppg = float(check.ppg),
                        rebounds = float(check.rebounds),
                        assists = float(check.assists),
                        per = float(check.per),
                        picture_url = "",
                        rating = 15
                    )
                    db.session.add(highscore)
                    db.session.commit()
                    payload = {"name": highscore.name, "ppg": highscore.ppg, "rebounds": highscore.rebounds, "assists": highscore.assists, "per": highscore.per}
            else:
                payload = {'error': 'Hmmm. Are you sure that is an NBA player?'}

            return jsonify(payload)
        except Exception as e:
            print(str(e))
            return jsonify(str(e))
    else:
        error = {'error': 'that player is already registered'}
        return jsonify(error)

@app.route("/pictures")
def get_pics():
    name = request.args.get('name')
    res_list = []
    player = Highscore.query.filter_by(name = name).first()
    if player is None:
        error = {'error': 'that player is not in the database'}
        return jsonify(error)
    else:
        client2 = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
        image_results = client2.images.search(query=name)
        image_list = image_results.value
        for image in image_list:
            res_list.append(image.content_url)
        res = Object()
        res.pics = res_list
        payload = res.toJSON()
        return jsonify(payload)

@app.route("/avatar", methods = ['POST'])
def add_avatar():
    name = request.args.get('name')
    picture_url = request.args.get('picture_url')
    player = Highscore.query.filter_by(name = name).first()
    if player is None:
        error = {'error': 'that player is not in the database'}
        return jsonify(error)
    else:
        player.picture_url = picture_url
        db.session.commit()
        return ""

@app.route("/videos")
def get_videos():
    name = request.args.get('name') + " best plays"
    res_list = []
    client3 = VideoSearchAPI(CognitiveServicesCredentials(subscription_key))
    video_results = client3.videos.search(query=name)
    videos_list = video_results.value
    for video in videos_list:
        res_list.append(video.content_url)
    res = Object()
    res.videos = res_list
    payload = res.toJSON()
    return jsonify(payload)

@app.route("/rating", methods = ['POST'])
def update_rating():
    name = request.args.get('name')
    rating = request.args.get('rating')
    player = Highscore.query.filter_by(name = name).first()
    if player is None:
        error = {'error': 'that player is not in the database'}
        return jsonify(error)
    else:
        player.rating = rating
        db.session.commit()
        return ""

@app.route("/getall")
def get_all():
    try:
        highscores=Highscore.query.all()
        return  jsonify([e.serialize() for e in highscores])
    except Exception as e:
	    return(str(e))

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    bypass = request.args.get('bypass')
    ip = request.args.get('ip')
    user = IP.query.filter_by(ip_address = ip).first()
    if bypass:
        res = {'count': user.count, 'timestamp': user.timestamp}
        return jsonify(res)
    if user is None:
        res = IP(ip_address= ip, count= 1)
        db.session.add(res)
        db.session.commit()
        res = {'count': res.count, 'timeStamp': res.timestamp}
        return jsonify(res)
    else:
        x = int(time.time())
        lockout = x - user.timestamp
        if user.count == 1 and lockout > 300:
            print('there')
            user.timestamp = int(time.time())
            db.session.add(user)
            db.session.commit()
            res = {'count': user.count, 'timestamp': user.timestamp}
            return jsonify(res)
        elif user.count == 1 and lockout < 300:
            print("here")
            user.count = 2
            db.session.add(user)
            db.session.commit()
            res = {'count': user.count, 'timestamp': user.timestamp}
            return jsonify(res)
        elif user.count == 2:
            if lockout > 300:
                user.timestamp = int(time.time())
                user.count = 1
                db.session.add(user)
                db.session.commit()
                res = {'count': user.count, 'timestamp': user.timestamp}
                return jsonify(res)
            else:
                res = {'count': 2, 'lockout': lockout}
                return jsonify(res)
        else:
            user.count = 2
            db.session.add(user)
            db.session.commit()
            res = {'count': user.count, 'timestamp': user.timestamp}
            return jsonify(res)


