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
    #https://www.statology.org/pandas-select-column-by-index/
    data = df
    return data.iloc[0,:]


def sorteer_data(data,column,ascending_bool):
    #https://blog.hubspot.com/website/pandas-sortby#:~:text=Pandas%20Sort%20by%20Column&text=Sorting%20data%20within%20a%20dataframe,the%20values%20in%20descending%20order.
    sorted_df = data.sort_values(by=(column), ascending=(ascending_bool))
    return sorted_df

data_list = laad_json_bestand('steam.json')
sorted_data = sorteer_data(data_list,'negative_ratings',True)
print((laad_eerste_game(sorted_data)))