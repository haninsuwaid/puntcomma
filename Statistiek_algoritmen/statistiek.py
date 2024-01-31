from basisfuncties.basisfuncties import data_naar_pandas#functie
from basisfuncties.onderzoek_data import freq#voor staafdiagram
import matplotlib.pyplot as plt
import numpy as np
import os

def kwantitatief_rapportcijfer_reviews(data):
    """
        Functie beschrijving:
            De functie berekend de waardering obv het totaal aantal gegeven negatieve en positieve beoordelingen
            en wordt uitgedrukt op een schaal van 10.
        Parameters:
            Data: Pandas Dataframe
        Return:
            Een bijgewerkte Pandas Dataframe, met toegevoegde kolommen per game voor het totaal gegeven beoordelingen en
            de waarding.
    """

    data['totaal_ratings'] = data['positive_ratings'] + data['negative_ratings']
    data['cijfer'] = round((data['positive_ratings'] / data['totaal_ratings']) * 10, 1)

    return data

def plot_staafdiagram_rapportcijfers(data,key):
    """
        Functie beschrijving:
            Deze functie visualiseert het aantal games per bijbehorend rapportcijfer in de vorm van een histogram.
        Parameters:
            Data: Pandas dataframe.
        Return:
            Histogram.
    """
    freqs = freq(data,(key))
    lst = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

    telling = {}

    for i in lst:
        som = 0
        for key, value in freqs.items():
            if i - 0.5 < key and key <= i:
                som += value

        telling[i] = som

    plt.figure(figsize=(15, 15))
    plt.figure(facecolor='#1b2838')
    plt.bar(list(telling.keys()), telling.values(), width=0.4, color='#354f52', edgecolor='white')
    plt.xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
               , rotation=45, ha='right')
    plt.ylabel('Aantal Games', color="white")
    plt.title('Rapportcijfers', color="white")
    plt.yticks(color="white")
    plt.xticks(color="white")

    graph_rapportcijfer = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static','images', 'graph_rapportcijfers'))
    plt.savefig(graph_rapportcijfer)
    plt.close()
    return graph_rapportcijfer

def plot_insight_ratings_per_game(data, game_id):
    """
        Functie beschrijving:
            Deze functie visualiseert het aantal negatieve en positieve beoordelingen van een game door middel van een cirkeldiagram.
            Tevens wordt het totaal aantal gegeven beoordelingen van deze game weergegeven.
        Parameters:
            Data: Pandas dataframe.
            Game_id: ID van de game
        Return:
            Cirkeldiagram
        Bronnen:
            - https://www.w3schools.com/python/matplotlib_pie_charts.asp
            - https://www.w3schools.com/colors/colors_names.asp
    """
    game_data = data[data['appid'] == game_id]
    positief = game_data['positive_ratings'].iloc[0]
    negatief = game_data['negative_ratings'].iloc[0]#.iloc[0] wordt gebruikt om de value om te zetten naar een enkele waarde
    totaal_ratings = game_data['totaal_ratings'].iloc[0]

    y = np.array([positief, negatief])
    mylabels = ['Positief', 'Negatief']
    mycolors = ["#354f52", "#1b2838"]

    # Create a figure with a white background
    fig, ax = plt.subplots(facecolor='#1b2838')

    ax.pie(y, labels=mylabels, colors=mycolors, autopct='%1.1f%%', startangle=90,textprops={'color':'white'})


    plt.title(f'{game_data["name"].iloc[0]} (ID: {game_id})\nVerdeling over de totaal gegeven ratings: {totaal_ratings}', color='white')
    plt.tight_layout()

    #sla figuur op
    graph_ratings_game = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'graph_ratings_{game_id}.png'))
    plt.savefig(graph_ratings_game)


    plt.close()

    return graph_ratings_game

#--------------------------------------------------------------------------------------------------------------------------------#
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'json', 'new_steam.json'))
df = data_naar_pandas(json_path)
new_data = kwantitatief_rapportcijfer_reviews(df)
plot_insight_ratings_per_game(new_data,20)

#new_data = kwantitatief_rapportcijfer_reviews(df)
#pandas_naar_json(new_data,'new_steam_data.json')