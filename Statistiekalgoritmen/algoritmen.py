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
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

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


def kwantitatief_rapportcijfer_reviews(data):
    data['totaal_ratings'] = data['positive_ratings'] + data['negative_ratings']
    data['cijfer'] = round((data['positive_ratings'] / data['totaal_ratings']) * 10, 1)
    gesorteerde_data = data.sort_values(by='totaal_ratings', ascending=False)
    top_100 = gesorteerde_data.head(100)

    return top_100

def gradient_descent(prijs, rating, num_iterations=1000, learning_rate=0.0001):
    a = 0
    b = 0

    for aantal in range(num_iterations):
        for i in range(len(prijs)):
            error = (a + b * prijs[i]) - rating[i]
            a -= error * learning_rate
            b -= prijs[i] * error * learning_rate

    coefficients = [a, b]
    nieuwe_prijzen = [0.0, 10, 50]
    # voorspellingen = [coefficients[0] + coefficients[1] * prijs for prijs in nieuwe_prijzen]
    #
    # print("Voorspelde cijfers voor nieuwe prijzen:", voorspellingen)

    return coefficients

data = laad_json_bestand()
top_100_meest_gereviewde_games = kwantitatief_rapportcijfer_reviews(data)
prijs = top_100_meest_gereviewde_games["price"].tolist()
rating = top_100_meest_gereviewde_games["cijfer"].tolist()
# coefficients = gradient_descent(prijs, rating)
# print("Gevonden coëfficiënten:", coefficients)

"""
    functie beschrijving:
        De functie gaat de frequentie berekenen van de top 10 genres, om te zien
        hoevaak elke genre het meest voorkomen in games

    parameters:
        geen

    return:
        De frequentie van de top 10 genre
"""
def kwalitatief_frequentie_genres():
    data = laad_json_bestand()
    genres = data['genres']
    lst = []
    for gen in genres:
        genre = gen.split(';')
        lst.append(genre)
    flat_list = []
    for sublist in lst:
        flat_list.extend(sublist)
    frequentie_genres = {}
    for item in flat_list:
        if item in frequentie_genres:
            frequentie_genres[item] += 1
        else:
            frequentie_genres[item] = 1

    sorted_items = sorted(frequentie_genres.items(), key=lambda x: x[1], reverse=True)
    top_10 = dict(sorted_items[:10])

    game_genre = list(top_10.keys())
    values = list(top_10.values())

    fig = plt.figure(figsize=(10, 10))
    plt.figure(facecolor='#1b2838')
    plt.barh(game_genre, values, color='#354f52', height=0.7)
    plt.yticks(color="white")
    plt.xticks(color="white")


    plt.xlabel("Aantal games", color='white')
    plt.ylabel("Genres", color='white')
    plt.title("Hoevaak games voorkomen in elke genre", color='white')
    # plt.show()
    file_path = 'static\images\graph_genre.png'
    plt.savefig(file_path)
    plt.close()
    return file_path


"""
    functie beschrijving:
        De functie gaat de frequentie berekenen van de prijzen van de games, om te zien
        hoevaak elke prijcategorie voorkomt op de steam applicatie

    parameters:
        df: de functie die de data van het json bestand opent en inlaadt

    return: frequentie_prijs
"""
def kwantitatief_frequentie_prijs():
    price_data = laad_json_bestand()
    prijzen = price_data['price']

    free = len([prijs for prijs in prijzen if prijs == 0])
    under_5 = len([prijs for prijs in prijzen if 0.01 <= prijs < 5])
    between_5_and_10 = len([prijs for prijs in prijzen if 5 <= prijs < 10])
    between_10_and_30 = len([prijs for prijs in prijzen if 10 <= prijs < 30])
    between_30_and_60 = len([prijs for prijs in prijzen if 30 <= prijs < 60])
    over_60 = len([prijs for prijs in prijzen if prijs > 60])

    prijsfrequentie = {
        "Gratis": free,
        "\u20AC0 - \u20AC5": under_5,
        "\u20AC5 - \u20AC10": between_5_and_10,
        "\u20AC10 - \u20AC30": between_10_and_30,
        "\u20AC30 - \u20AC60": between_30_and_60,
        "Over \u20AC60": over_60
    }

    fig = plt.figure(figsize=(10, 10))
    plt.figure(facecolor='#1b2838')

    x = np.array(list(prijsfrequentie.keys()))
    y = np.array(list(prijsfrequentie.values()))
    plt.bar(x, y, color='#354f52')
    plt.yticks(color="white")
    plt.xticks(color="white")
    plt.title("Aantal games per prijscategorie", color='white')
    plt.xlabel("Prijscategorieën", color='white')
    plt.ylabel("Aantal games", color='white')

    graph_filename = 'static\images\graph_price.png'
    plt.savefig(graph_filename)
    plt.close()
    return graph_filename

def achievement_playtime(num_iterations=1000, learning_rate=0.0001):
    """
        functie beschrijving:
            De functie gaat door gebruik te maken van een linear regression voorspellen hoe vaak games worden gespeeld.
            Dit word berekend door gebruik te maken van de hoeveelheid achievements,
            en hoeveel uur een game wordt gespeeld


        parameters:
            num_iterations: De hoeveelheid iteraties het algortime gaat runnen
            learning_rate: de grootte van de stappen voor de iteratie

        return: a, b
    """
    json_data = laad_json_bestand()

    x = json_data['achievements'].tolist()
    y = json_data['average_playtime'].tolist()

    a = 0
    b = 0
    for _ in range(num_iterations):
        for i in range(len(x)):
            if 500 > x[i] > 0 and y[i] > 0:
                error = (a + b * x[i]) - y[i]
                a = a - error * learning_rate
                b = b - x[i] * error * learning_rate

    return a, b
# print(achievement_playtime())
