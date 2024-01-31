from flask import request, session, redirect, url_for, jsonify, render_template, Flask
from Statistiekalgoritmen.algoritmen import *
from Statistiekalgoritmen.apiJson import *
from basisfuncties.onderzoek_data import *
from views import views


app = Flask(__name__, template_folder='templates')

app.register_blueprint(views, url_prefix="/views")

app.secret_key = 'geheim'


@app.route('/', methods=['GET', 'POST'])
def landing_page():
    """
        Functie beschrijving:
            this function sends the user to the landingspage where the user has to fill their key and steamid
            after they log in a session starts. with the POST method. The function gets the key and steamid
            from the form. After that the user get sent to the profile page.
        Return:
            the landingspage
    """
    if request.method == 'POST':
        session['steamid'] = request.form['steamid']
        session['key'] = request.form['key']
        return redirect(url_for('profile'))
    return render_template('landingspage.html')


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    """
        Functie beschrijving:
            this fucntion first checks if there is a POST request from the form if yes it gets the key and
            steam id and uses it for the session. If the request is not compliet the user get sent to the
            landingspage.
            another function needed for the profile page are also called from app.py.
        Return:
            the profile page with the called functions for that page
    """
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
    """
        Functie beschrijving:
            this function gets functions from another files to display the returned data.
        Return:
            the page path and the needed functions for that page
    """
    game_info = info_for_steam_games()
    return render_template('home.html', game_info=game_info)


@app.route('/game/<appid>')
def game(appid):
    """
        Functie beschrijving:
            a function that gets the appid of a chosen game and the function steam_game_info uses the id
            to get the game data with the function.
        Parameters:
            appid: the id of a chosen game from the url
        Return:
            the path of the game page and the function
    """
    games_data = steam_game_info(appid)
    return render_template('game.html', game=games_data)


@app.route('/stats/')
def stats():
    """
        Functie beschrijving:
            fucntion to render the stats.html page
        Return:
            returns the path of that page
    """
    achievements_playtime = achievement_playtime()
    frequentie_prijs = kwantitatief_frequentie_prijs()
    frequentie_genres = kwalitatief_frequentie_genres()
    linear_regression_price = linear_regression_price_rating()

    df = laad_json_bestand()
    results = onderzoek_data(df, 'cijfer')
    sorteer_data_data = sorteer_data(df, 'negative_ratings', True)
    return render_template('stats.html', linear_regression_price=linear_regression_price, frequentie_genres=frequentie_genres, frequentie_prijs=frequentie_prijs, achievements_playtime=achievements_playtime, sorteer_data_data=sorteer_data_data, results=results )


@app.route('/owned_games/')
def owned_games():
    """
        Functie beschrijving:
            this function gets the key and steamid from the session. and it gets the appid.
            So they could be used in the parameters of the owned_games_info function.
        Return:
            the path of the owned_game page with the needed fucntions in that page
    """
    key = session.get('key')
    steamid = session.get('steamid')
    appid = request.args.get('appid')
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


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

    # B129420016573EE260056E21D4218C90
    # 76561198366424343