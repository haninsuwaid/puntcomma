from flask import Flask, render_template, request, session, redirect, url_for
from Statistiekalgoritmen.algoritmen import *
from Statistiekalgoritmen.apiJson import *
from views import views

app = Flask(__name__, template_folder='templates')

app.register_blueprint(views, url_prefix="/views")

app.secret_key = 'geheim'

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        session['steamid'] = request.form['steamid']
        session['key'] = request.form['key']
        return redirect(url_for('profile'))
    return render_template('landingspage.html')


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        steamid = request.form['steamid']
        key = request.form['key']
        session['steamid'] = steamid
        session['key'] = key
    steamid = session.get('steamid')
    key = session.get('key')
    if not steamid or not key:
        return redirect(url_for('landing_page'))
    user_profile = user(key, steamid)
    owned_games = amount_owned_games(key, steamid)
    owned_game_info = owned_games_info(key, steamid, limit=20)
    friend_list_info = friends_list_info(key, steamid, limit=5)
    return render_template('profile.html', user_profile=user_profile, owned_games=owned_games,
                           friend_list_info=friend_list_info, owned_game_info=owned_game_info)


@app.route('/home/')
def home():
    df = laad_json_bestand()
    eerste_game = laad_eerste_game(df)
    sorteer_data_data = sorteer_data(df, 'negative_ratings', True)
    prijsfrequentie = kwantitatief_frequentie_prijs()
    chart_image = kwalitatief_frequentie_genres()
    all_steam_game = all_steam_games(limit=10)
    game_info = [steam_game_info(game["appid"]) for game in all_steam_game]
    return render_template('home.html', eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie, chart_image=chart_image, all_steam_game=all_steam_game, game_info=game_info)


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
    game_info = [steam_game_info(game["appid"]) for game in all_steam_game]
    return render_template('owned_games.html', appid=appid, game_info=game_info, game_name=game_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    # B129420016573EE260056E21D4218C90
    # 76561198366424343