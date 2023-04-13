from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# my_url = SITE_ROOT + "/static/pokedex.json"
# print(my_url)
# pokedex = json.load(open(my_url))
# g.pokedex = pokedex

from . import routes


