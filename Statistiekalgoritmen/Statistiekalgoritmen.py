from basisfuncties import *
import numpy as np
import matplotlib.pyplot as plt

def kwantitatief_rapportcijfer_reviews(data):
    """
        Functie beschrijving:
            De functie berekend de waardering obv het totaal aantal gegeven negatieve en positieve reviews.
            De waardering wordt uitgedrukt op een schaal van 10.

        Parameters:
            Data: Panda dataframe

        Return:
            Een Panda DataFrame bestaande uit de keys 'naam', 'rapportcijfer' en 'totaal_ratings'. De DataFrame wordt
            gesorteerd op zowel het hoogste rapportcijfer als het grootste aantal totaal_ratings.
    """

    data['totaal_ratings'] = data['positive_ratings'] + data['negative_ratings']
    data['cijfer'] = round((data['positive_ratings'] / data['totaal_ratings']) * 10, 1)

    return sorteer_data(data, 'cijfer', False)

def plot_histogram_rapportcijfers(data):
    #Afmetingen figuur
    plt.figure(figsize=(10, 6))

    #Maak Historgram
    plt.hist(data['cijfer'], bins=20, color='black', alpha=1, edgecolor='grey')

    #x,y,titelnaam
    plt.xlabel('Rapportcijfer')
    plt.ylabel('Aantal Games')
    plt.title('Rapportcijfers')

    plt.xticks(np.arange(0, 10.5, 0.5))

    graph_rapportcijfer = "/Users/beaugunther/PycharmProjects/puntcomma/static/images/graph_rapportcijfer.png"
    plt.savefig(graph_rapportcijfer)
    plt.close()
    return graph_rapportcijfer

def plot_insight_ratings_per_game(data, game_id):
    game_data = data[data['appid'] == game_id]
    positief = game_data['positive_ratings'].iloc[0]
    negatief = game_data['negative_ratings'].iloc[0]#.iloc[0] wordt gebruikt om de value om te zetten naar een enkele waarde
    totaal_ratings = game_data['totaal_ratings'].iloc[0]

    y = np.array([positief, negatief])
    mylabels = ['Positief', 'Negatief']

    plt.pie(y, labels=mylabels, autopct='%1.1f%%', startangle=90)

    plt.title(f' {game_data["name"].iloc[0]} (ID: {game_id})\nVerdeling over de totaal gegeven ratings: {totaal_ratings}')

    graph_ratings_game = "/Users/beaugunther/PycharmProjects/puntcomma/static/images/graph_ratings_game.png"
    plt.savefig(graph_ratings_game)
    plt.close()
    return graph_ratings_game


df = laad_json_bestand('/Users/beaugunther/PycharmProjects/puntcomma/json/steam.json')
new_data = kwantitatief_rapportcijfer_reviews(df)
#from_panda_to_json(new_data,'new_steam.json')
plot_histogram_rapportcijfers(new_data)
plot_insight_ratings_per_game(new_data,20)
