from flask import Flask, render_template
from Statistiekalgoritmen.algoritmen import *
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
<<<<<<< Updated upstream
    return render_template('home.html', eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie, chart_image=chart_image)
=======
    game_info = info_for_steam_games()
    return render_template('home.html', eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie, chart_image=chart_image, game_info=game_info)


@app.route('/game/<appid>')
def game(appid):
    games_data = steam_game_info(appid)
    return render_template('game.html', game=games_data)


@app.route('/stats/')
def stats():
    return render_template('stats.html')

@app.route('/owned_games/')
def owned_games():
    key = session.get('key')
    steamid = session.get('steamid')
    appid = request.args.get('appid')
    all_steam_game = all_steam_games(limit=15)
    game_name = owned_games_info(key, steamid, limit=15)
    game_info = info_for_steam_games()
    return render_template('owned_games.html', appid=appid, game_info=game_info, game_name=game_name)

#rick's meuk

@app.route("/test_profile/<key>/<user_id>", methods = ['POST'])
def test_profile(key, user_id):
    user_profile = user_by_id(key, user_id)
    return jsonify(user_profile)

@app.route("/test_games/<key>/<user_id>", methods = ['POST'])
def test_games(key, user_id):
    user_games = all_owned_games(key, user_id)
    return jsonify(user_games)


@app.route("/test_amount_of_games/<key>/<user_id>", methods=['POST'])
def test_amount_of_games(key, user_id):
    amount_user_games = amount_owned_games(key, user_id)
    return jsonify(amount_user_games)
>>>>>>> Stashed changes


if __name__ == '__main__':
    app.run(debug=True, port=5000)