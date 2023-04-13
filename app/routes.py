from flask import render_template, request
from app import app
from app.forms import PokeSearchForm
import requests
import json
from thefuzz import process as fuzzprocess
import os

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/pokesearch',methods=["GET","POST"])
def pokesearch():
    form = PokeSearchForm()
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.pokemon_name.data.strip().lower()
            poke_results = find_poke(pokemon_name)
            if not poke_results:
                pokeguess = poke_suggest(pokemon_name)
                return render_template('pokesearch.html',form=form,not_valid_pokemon = pokemon_name,pokeguess=pokeguess)
            else:
                return render_template('pokesearch.html',form=form,poke_results=poke_results)

    return render_template('pokesearch.html',form=form)

def poke_suggest(pokemon_name):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    my_url = SITE_ROOT + "/static/pokedex.json"
    pokedex = json.load(open(my_url))
    pokeguess,_ = fuzzprocess.extractOne(pokemon_name,pokedex.keys())
    print(pokeguess)
    return pokeguess
    
def find_poke(pokemon_name):
    pokemon_name = pokemon_name.strip().lower()
    if not pokemon_name:
        return False
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
    response = requests.get(url)
    if not response.ok:
        return False

    data = response.json()
    poke_dict={
            "poke_id": data['id'],
            "name": data['name'].title(),
            "ability":data['abilities'][0]["ability"]["name"],
            "base experience":data['base_experience'],
            "photo":data['sprites']['other']['home']["front_default"],
            "attack base stat": data['stats'][1]['base_stat'],
            "hp base stat":data['stats'][0]['base_stat'],
            "defense stat":data['stats'][2]["base_stat"]}
    return poke_dict