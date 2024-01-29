from flask import Flask, render_template
from basisfuncties import data_naar_pandas#functie
from basisfuncties import json_path#bestand
from Statistiek_algoritmen.statistiek import plot_staafdiagram_rapportcijfers,plot_insight_ratings_per_game
from views import views


app = Flask(__name__, template_folder='templates')

app.register_blueprint(views, url_prefix="/views")

@app.route('/')
def home():
    df = data_naar_pandas(json_path)
    rapportcijfers_staafdiagram = plot_staafdiagram_rapportcijfers(df,'cijfer')
    ratings_game = plot_insight_ratings_per_game(df,20)
    return render_template('home.html', rapportcijfers_staafdiagram=rapportcijfers_staafdiagram,ratings_game=ratings_game)


if __name__ == '__main__':
    app.run(debug=True, port=5000)