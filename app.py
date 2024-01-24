from flask import Flask, render_template
from Statistiekalgoritmen.algoritmen import *
from Statistiekalgoritmen.apiJson import *
from views import views
import pandas as pd
import json
import os

app = Flask(__name__, template_folder='templates')

app.register_blueprint(views, url_prefix="/views")

@app.route('/')
def home():
    df = laad_json_bestand()
    eerste_game = laad_eerste_game(df)
    sorteer_data_data = sorteer_data(df, 'negative_ratings', True)
    prijsfrequentie = kwantitatief_frequentie_prijs()
    chart_image = kwalitatief_frequentie_genres()
    all_steam_game = all_steam_games(limit=10)
    return render_template('home.html', eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie, chart_image=chart_image, all_steam_game=all_steam_game)


@app.route('/game/<appid>')
def game(appid):
    games_data = steam_game_info(appid)
    return render_template('game.html', game=games_data)

@app.route('/profile/')
def profile():
    user_profile = user()
    owned_games = amount_owned_games()
    owned_game_info = owned_games_info(limit=20)
    return render_template('profile.html', user_profile=user_profile, owned_game_info=owned_game_info, owned_games=owned_games)


if __name__ == '__main__':
    app.run(debug=True, port=5000)