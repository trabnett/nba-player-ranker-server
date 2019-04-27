# nba-player-ranker-server

Server for a simple onepage react app that lets users rank their favorite NBA players. Uses Microsoft Azure to search for relevant player data, pictures and videos. Uses BeautifulSoup to scrape data from Basketball Reference. Uses Postgres for data storage.

webapp is hosted on heroku at:
[NBA Player Ranker webapp](https://nba-player-ranker.herokuapp.com/)

code for webapp at:
[NBA Player Ranker webapp code](https://github.com/trabnett/nba_player_ranker_webapp)

server is hosted on heroku at:
[NBA Player Ranker server](https://player-ranker-server.herokuapp.com/)

#### employs:

+ Flask
+ Microsoft Azure
+ Beautiful Soup
+ Postgres

#### Quick Start
1. Clone the repo  
``
 $ git clone https://github.com/trabnett/nba-player-ranker-server
``  
``
 $ cd nba-player-ranker-server
``

2. Initialize and activate a virtualenv  
``
$ virtualenv venv
``
``
$ source venv/bin/activate
``
3. Install dependencies  
``
$ pip install -r requirements.txt
``
4. Migrage db  
``
flask db migrate -m "highscore"
``
5. Run the development server  
``
flask run
``
