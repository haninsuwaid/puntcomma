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
    return render_template('home.html',eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie, chart_image=chart_image)

@app.route('/profile/')
def profile():
    user_profile = user()
    owned_games = all_owned_games()
    return render_template('profile.html', user_profile=user_profile, owned_games=owned_games)


@app.route('/owned_games/')
def owned_games():
    ownedgames = all_owned_games()
    return render_template('owned_games.html', ownedgames=ownedgames)

if __name__ == '__main__':
    app.run(debug=True, port=5000)