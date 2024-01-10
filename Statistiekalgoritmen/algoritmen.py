"""
    Hier gaan wij een lege functie maken met parameters, en de return. Daarbij gaan we ook uitleg
    schrijven over wat de functie doet, waar de parameters voor gebruikt worden,
    en wat de functie uiteindelijk returnt. Alleen dus Statistiekalgoritmen van
    de verplichte onderdelen van Ai.
"""

import pandas as pd
import json
import os
from flask import Flask, render_template


def laad_json_bestand():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'puntcomma', 'json', 'steam.json')
    with open(json_path) as bestand:
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


def sorteer_data(data, column, ascending_bool):
    sorted_df = data.sort_values(by=(column), ascending=(ascending_bool))
    return sorted_df


"""
    functie beschrijving:
        De functie gaat de gemiddelde uitrekenen van de reviews van games

    parameters:
        data: data die mee wordt uitgerekend om de gemiddelde uit te halen.

    return:
        De gemiddelde van game review
"""
# def kwantitatief_gemiddelde_reviews(positieve_reviews, negatieve_reviews):

    #return gemiddelde_review


"""
    functie beschrijving:
        De functie gaat de frequentie berekenen van de genres, om te zien
        hoevaak elke genre het meest voorkomen in games

    parameters:
        genres: de genres die worden opgehaald.

    return:
        De frequentie van elke genre
"""
def kwatitatief_frequentie_genres():
    data = laad_json_bestand()
    genres = data['genres']
    lst = []
    for gen in genres:
        genre = gen.split(';')
        lst.append(genre)
    flat_list = []
    for sublist in lst:
        flat_list.extend(sublist)
    frequentie = {}
    for item in flat_list:
        if item in frequentie:
            frequentie[item] += 1
        else:
            frequentie[item] = 1
    return frequentie

genre_frequencies = kwatitatief_frequentie_genres()
print(genre_frequencies)
#def kwatitatief_frequentie_genres(genres):
#return genre_frequentie

"""
    functie beschrijving:


    parameters:


    return: frequentie_prijs
"""
# def kwantitatief_frequentie_prijs():

    #return frequentie_prijs