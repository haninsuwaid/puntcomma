import pandas as pd
import json


def laad_json_bestand(bestandsnaam):
    #https://saturncloud.io/blog/how-to-convert-nested-json-to-pandas-dataframe-with-specific-format/
    with open('json/steam.json') as bestand:
        data = json.load(bestand)

    # pd.json_normalize convert the JSON to a DataFrame
    df = pd.json_normalize(data,
                           meta=["appid", "name", "name", "english", "developer", "publisher", "platforms",
                                 "required_age", "categories", "genres", "steamspy_tags",
                                 "achievements", "positive_ratings", "negative_ratings", "average_playtime",
                                 "median_playtime", "owners", "price"])
    return df

def laad_eerste_game(df):
    data = df
    return df.iloc[0,:]#index 0, all columns
    #https://www.statology.org/pandas-select-column-by-index/


data_list = laad_json_bestand('steam.json')
(laad_eerste_game(data_list))