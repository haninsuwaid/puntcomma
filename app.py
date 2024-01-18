from flask import Flask, render_template
from views import views
import pandas as pd
import json

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")


def laad_json_bestand():
    with open('json/steam.json') as bestand:
        data = json.load(bestand)

    df = pd.json_normalize(data,
                           meta=["appid", "name", "name", "english", "developer", "publisher", "platforms",
                                 "required_age", "categories", "genres", "steamspy_tags",
                                 "achievements", "positive_ratings", "negative_ratings", "average_playtime",
                                 "median_playtime", "owners", "price"])
    return df

def laad_eerste_game(df):
    data = df
    return data.iloc[0, :]



@app.route('/')
def home():
    df = laad_json_bestand()
    eerste_game = laad_eerste_game(df)

    return render_template('home.html', eerste_game=eerste_game)

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
