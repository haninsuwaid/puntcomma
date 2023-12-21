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
    prijsfrequentie = kwantitatief_frequentie_prijs(df)
    return render_template('home.html', eerste_game=eerste_game, sorteer_data_data=sorteer_data_data, prijsfrequentie=prijsfrequentie)


if __name__ == '__main__':
    app.run(debug=True, port=5000)