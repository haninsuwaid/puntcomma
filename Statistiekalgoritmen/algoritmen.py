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

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'puntcomma', 'json', 'steam.json')
def laad_json_bestand():
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
#def kwatitatief_frequentie_genres(genres):
#return genre_frequentie


def kwantitatief_frequentie_prijs(df):
    """
        functie beschrijving:
            De functie gaat de frequentie berekenen van de prijzen van de games, om te zien
            hoevaak elke prijcategorie voorkomt op de steam applicatie

        parameters:
            df: de functie die de data van het json bestand opent en inlaadt

        return: frequentie_prijs
    """

    free = len(df[df["price"] == 0])
    under_5 = len(df[(df["price"] >= 0.01) & (df["price"] < 5)])
    between_5_and_10 = len(df[(df["price"] >= 5) & (df["price"] < 10)])
    between_10_and_30 = len(df[(df["price"] >= 10) & (df["price"] < 30)])
    between_30_and_60 = len(df[(df["price"] >= 30) & (df["price"] < 60)])
    over_60 = len(df[df["price"] > 60])
    frequentie_prijs = free, under_5, between_5_and_10, between_10_and_30, between_30_and_60, over_60

    return frequentie_prijs