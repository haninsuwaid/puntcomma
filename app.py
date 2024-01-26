from flask import Flask, render_template
from Statistiekalgoritmen.algoritmen import *
from basisfuncties import *
from Statistiekalgoritmen.statistiek import *
from views import views
import pandas as pd
import json
import os

app = Flask(__name__, template_folder='templates')

app.register_blueprint(views, url_prefix="/views")

@app.route('/')
def home():
    df = laad_json_bestand(json_path)
    eerste_game = laad_eerste_game(df)
    sorteer_data_data = sorteer_data(df, 'negative_ratings', True)
    prijsfrequentie = kwantitatief_frequentie_prijs()
    chart_image = kwalitatief_frequentie_genres()
    rapportcijfers_staafdiagram = plot_staafdiagram_rapportcijfers(df,'cijfer')
    ratings_game = plot_insight_ratings_per_game(df,20)
    return render_template('home.html', eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie, chart_image=chart_image, rapportcijfers_staafdiagram=rapportcijfers_staafdiagram,ratings_game=ratings_game)


if __name__ == '__main__':
    app.run(debug=True, port=5000)