import pandas as pd
import json


def laad_json_bestand(bestandsnaam):
    """Deze functie converteert de data naar een panda dataframe"""
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
    """Deze functie selecteert de eerste game"""
    #https://www.statology.org/pandas-select-column-by-index/
    data = df
    return data.iloc[0,:]#[index,alle kolommen]


def sorteer_data(data,column,ascending_bool):
    """Deze functie sorteert de data obv de opgegeven parameters"""
    #https://blog.hubspot.com/website/pandas-sortby#:~:text=Pandas%20Sort%20by%20Column&text=Sorting%20data%20within%20a%20dataframe,the%20values%20in%20descending%20order.
    sorted_df = data.sort_values(by=(column), ascending=(ascending_bool))
    return sorted_df

data_list = laad_json_bestand('steam.json')#laadt data in panda dataframe
sorted_data = sorteer_data(data_list,'negative_ratings',True)#geef 3 parameters op; data, kolomnaam, ascending; true or false
print((laad_eerste_game(sorted_data)))

#https://realpython.com/pandas-sort-python/#:~:text=the%20first%20rows.-,Choosing%20a%20Sorting%20Algorithm,quicksort%20%2C%20mergesort%20%2C%20and%20heapsort%20.
#https://www.statology.org/pandas-groupby-index/