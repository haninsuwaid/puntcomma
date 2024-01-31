"""
    Hier gaan wij een lege functie maken met parameters, en returns. Daarbij gaan we ook uitleg
    schrijven over wat de functie doet, waar de parameters voor gebruikt worden,
    en wat de functie uiteindelijk returnt. Alleen dus van Ai.
"""
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import numpy as np


def laad_json_bestand():
    """
        Functiebeschrijving:
            Deze functie laadt JSON-gegevens uit een bestand of een lijst, en converteert deze naar een Pandas DataFrame.
            Het bestand kan zowel een JSON-bestand als een lijst met JSON-objecten zijn.
        Parameters:
            Bestandsnaam: JSON-bestand of lijst.
        Return:
            Pandas Dataframe.
    """
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'puntcomma', 'json', 'new_steam.json')
    with open(json_path) as bestand:
        data = json.load(bestand)

    df = pd.json_normalize(data,
                           meta=["appid", "name", "name", "english", "developer", "publisher", "platforms",
                                 "required_age", "categories", "genres", "steamspy_tags",
                                 "achievements", "positive_ratings", "negative_ratings", "average_playtime",
                                 "median_playtime", "owners", "price"])
    return df


def kwantitatief_rapportcijfer_reviews(data):
    """
        Functie beschrijving:
            De functie berekend de waardering obv het totaal aantal gegeven negatieve en positieve beoordelingen
            en wordt uitgedrukt op een schaal van 10. Het wordt ook gesorteerd op de top 200 meest beoordeelde games.
        Parameters:
            Data: Pandas Dataframe
        Return:
            Een bijgewerkte Pandas Dataframe, met toegevoegde kolommen per game voor het totaal gegeven beoordelingen en
            de waarding.
    """
    data['totaal_ratings'] = data['positive_ratings'] + data['negative_ratings']
    data['cijfer'] = round((data['positive_ratings'] / data['totaal_ratings']) * 10, 1)
    gesorteerde_data = data.sort_values(by='totaal_ratings', ascending=False)
    top_100 = gesorteerde_data.head(200)

    return top_100


def gradient_descent(prijs, rating, num_iterations=1000, learning_rate=0.0001):
    """
        functie beschrijving:
            A function that calculates the coefficients using two lists: prijs and rating.
            The dependent values are the ratings, and the independent values are the prices.
        parameters:
            prijs: A list of prices of the top most played games.
            rating: A list of rating from 0 to 10 of the most rated games.
            num_interations: the amount of interations the function needs to find the coefficients
            learing_rate: how much the coefficients should change everytime to find the coefficients
        return:
            The coefficients
    """
    a = 0
    b = 0

    for iteration in range(num_iterations):
        for i in range(len(prijs)):
            error = (a + b * prijs[i]) - rating[i]
            a -= error * learning_rate
            b -= prijs[i] * error * learning_rate
    coefficients = [a, b]
    return coefficients

"""
    The data I want to give to the gradient_descent function
"""
data = laad_json_bestand()
top_100_meest_gereviewde_games = kwantitatief_rapportcijfer_reviews(data)
prijs = top_100_meest_gereviewde_games["price"].tolist()
rating = top_100_meest_gereviewde_games["cijfer"].tolist()


coefficients = gradient_descent(prijs, rating)
a, b = coefficients


def linear_regression(x):
    """
        functie beschrijving:
            this function is a linear regression formula. It calculates the predicted value.
            outside the function I give a and b values form the coefficients of the gradient_descent function
        parameters:
            x: the independent value the price in this case
        return:
            linear regression formula
    """
    return a + b * x


def linear_regression_price_rating():
    """
        functie beschrijving:
            this fucntion makes a graph with data points, and the line of the linear_regression.
        return:
            De file_path waar de staafdiagram wordt opgeslagen.
    """
    plt.figure(facecolor='#1b2838')
    plt.scatter(prijs, rating, color='#354f52', label='Data points')
    plt.plot(prijs, linear_regression(np.array(prijs)), 'red', label='Linear Regression')
    plt.yticks(color="white")
    plt.xticks(color="white")
    plt.ylabel('Rating', color='white')
    plt.xlabel('Price', color='white')
    plt.legend()
    file_path = 'static\images\linear_regression_price_rating.png'
    plt.savefig(file_path)
    plt.close()
    return file_path


def kwalitatief_frequentie_genres():
    """
        functie beschrijving:
            De functie gaat de frequentie berekenen van de top 10 genres, om te zien
            hoevaak elke genre het meest voorkomen in games. Op basis van de resultaten, maak ik staafdiagram
            met de frequentie van de top 10 genres met de meeste games. De grafiek wordt gestyled en opgeslagen.
        parameters:
            geen
        return:
            De file_path waar de staafdiagram wordt opgeslagen.
    """
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
    plt.figure(facecolor='#1b2838')
    plt.barh(game_genre, values, color='#354f52', height=0.7)
    plt.yticks(color="white")
    plt.xticks(color="white")
    plt.xlabel("Aantal games", color='white')
    plt.ylabel("Genres", color='white')
    plt.title("Hoevaak games voorkomen in elke genre", color='white')
    file_path = 'static\images\graph_genre.png'
    plt.savefig(file_path)
    plt.close()
    return file_path
    plt.figure(facecolor='#1b2838')
    plt.scatter(prijs, rating, color='blue', label='Data points')
    plt.plot(prijs, linear_regression(np.array(prijs)), 'k', label='Linear Regression')
    plt.yticks(color="white")
    plt.xticks(color="white")
    plt.ylabel('Rating', color='white')
    plt.xlabel('Price', color='white')
    plt.legend()
    file_path = 'static\images\linear_regression_price_rating.png'
    plt.savefig(file_path)
    plt.close()
    return file_path


def kwantitatief_frequentie_prijs():
    """
        function description:
            The function will calculate the frquency of the game prizes,
            To see how often each game appears in a price category on the steam application

        return: frequentie_prijs
    """

    # Loads the json file and put all the prices from the file in the var prijzen.
    price_data = laad_json_bestand()
    prijzen = price_data['price']

    # Loops all the prices and counts how many games are in the specific price range
    free = len([prijs for prijs in prijzen if prijs == 0])
    under_5 = len([prijs for prijs in prijzen if 0.01 <= prijs < 5])
    between_5_and_10 = len([prijs for prijs in prijzen if 5 <= prijs < 10])
    between_10_and_30 = len([prijs for prijs in prijzen if 10 <= prijs < 30])
    between_30_and_60 = len([prijs for prijs in prijzen if 30 <= prijs < 60])
    over_60 = len([prijs for prijs in prijzen if prijs > 60])

    # Creates a dictionary with the var "prijsfrequentie". This way its easy to access all the values in the plt
    prijsfrequentie = {
        "Gratis": free,
        "\u20AC0 - \u20AC5": under_5,
        "\u20AC5 - \u20AC10": between_5_and_10,
        "\u20AC10 - \u20AC30": between_10_and_30,
        "\u20AC30 - \u20AC60": between_30_and_60,
        "Over \u20AC60": over_60
    }

    plt.figure(facecolor='#1b2838')
    # Put the keys and values from the dictionary in the x and y for the price graph
    x = np.array(list(prijsfrequentie.keys()))
    y = np.array(list(prijsfrequentie.values()))

    # The styling and headings for the price graphs are shown here
    plt.bar(x, y, color='#354f52')
    plt.yticks(color="white")
    plt.xticks(color="white")
    plt.title("Aantal games per prijscategorie", color='white')
    plt.xlabel("Prijscategorieën", color='white')
    plt.ylabel("Aantal games", color='white')

    # Save the graph in the css map. Every time the function is used it will save it, so it stays updated.
    graph_filename = 'static\images\graph_price.png'
    plt.savefig(graph_filename)
    plt.close()
    return graph_filename


def achievement_playtime(num_iterations=1000, learning_rate=0.00001):
    """
        function description:
            This function uses a linear regression to predict how often games are played,
            Based on the amount of achievements a game has.


        parameters:
            num_iterations: The number of iterations the algorithm will run
            learning_rate: The size of the steps for the iteration

        return: a, b
    """

    # Get the data from the json and put the achievements in the x and the average playtime in the y
    # This .tolist() sets all the data automatically in a list
    json_data = laad_json_bestand()
    x = json_data['achievements'].tolist()
    y = json_data['average_playtime'].tolist()

    filtered_x = []
    filtered_y = []
    for i in range(len(x)):
        # Checks if a game has less than 500 achievements, more than 0 achievements,
        # and average playtime is not zero and under the 5000
        if 500 > x[i] > 0 and 5000 > y[i] > 10:
            # Append the games to a new list
            filtered_x.append(x[i])
            filtered_y.append(y[i])

    # Set the vars a and b on 0
    a = 0
    b = 0

    # Loops the amount of num_iterations
    for _ in range(num_iterations):
        # Loops through every game with achievements
        for i in range(len(filtered_x)):
            # Calculates the difference between the predicted value and the actual value
            error = (a + b * filtered_x[i]) - filtered_y[i]
            # Updates the coefficients a and b
            a = a - error * learning_rate
            b = b - filtered_x[i] * error * learning_rate

    filtered_x = np.array(filtered_x)
    model_line = a + b * filtered_x

    plt.figure(facecolor="#1b2838")
    plt.scatter(filtered_x, filtered_y, color="#354f52", label="Games")
    plt.plot(filtered_x, model_line, "red", label="Predicted playtime")
    plt.yticks(color="white")
    plt.xticks(color="white")
    plt.title('Prediction of the playtime based on achievements', color="white")
    plt.ylabel('Average Playtime', color="white")
    plt.xlabel('Achievements', color="white")
    plt.legend(loc="upper right")
    graph_filename = 'static\images\linear_regression_achievements_playtime.png'
    plt.savefig(graph_filename)
    plt.close()
    return a, b
