from basisfuncties import data_naar_pandas#functie
from basisfuncties import json_path#bestand
form basisfuncties import sorteer_data
from onderzoek_data import freq#voor staafdiagram
import matplotlib.pyplot as plt
import numpy as np
import os

def kwantitatief_rapportcijfer_pandas(data):
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
        De functie visualiseert de frequenties per rapportcijfer middels een staafdiagram. In het diagram wordt enkel
        onderscheidt gemaakt tussen halve cijfers. Zo dien je 0.5 te interpreteren als: vanaf 0 tot 0.5.

    Parameters:
        Data: Pandas dataframe.
        Key: Waarvan het diagram gevisualiseerd dient te worden.

    Return:
        Opgeslagen staafdiagram.

    Bron:
        • https://www.w3schools.com/python/matplotlib_bars.asp
        • https://www.youtube.com/watch?v=25zx2R1rCCg

    """
    freqs = freq(data,(key))
    lst = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

    telling = {}

    #loop om alle values binnen een range van 0.5, bij elkaar op te tellen
    for i in lst:
        som = 0
        for key, value in freqs.items():
            if i - 0.5 < key and key <= i:# i - 0.5 tot i
                som += value

        telling[i] = som

    plt.figure(figsize=(15, 15))
    plt.figure(facecolor='#1b2838')
    plt.title('Rapportcijfers', color="white")

    #definieer x en y
    x = list(telling.keys())
    y = list(telling.values())
    plt.bar(x,y, width=0.4, color='#354f52', edgecolor='white')
    plt.xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0], rotation=45, ha='right', color="white")
    plt.yticks(color="white")
    plt.ylabel('Aantal Games', color="white")

    #sla het figuur op
    graph_rapportcijfer = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static','images', 'graph_rapportcijfers'))
    plt.savefig(graph_rapportcijfer)
    #plt.show()
    plt.close()

    return graph_rapportcijfer

def plot_inzicht_waardering_per_game(data, game_id):
    """
    Functie beschrijving:
        Deze functie visualiseert het aantal positieve en negatieve beoordelingen van een game en weergeeft deze middels
        een cirkeldiagram. Tevens wordt het totaal aantal gegeven beoordelingen van de game weergegeven in de titel.

    Parameters:
        Data: Pandas dataframe.
        Game_id: ID van de game

    Return:
        Opgeslagen cirkeldiagram

    Bron:
        • https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
        • https://www.w3schools.com/python/matplotlib_pie_charts.asp
    """
    game_data = data[data['appid'] == game_id]#selecteer waar appid == game_id

    positief = game_data['positive_ratings'].iloc[0]#.iloc[0] daadwerkelijke waarde wordt geselecteerd
    negatief = game_data['negative_ratings'].iloc[0]
    totaal_ratings = game_data['totaal_ratings'].iloc[0]

    y = np.array([positief, negatief])
    mylabels = ['Positief', 'Negatief']
    mycolors = ["#354f52", "#1b2838"]

    fig, ax = plt.subplots(facecolor='#1b2838')
    ax.pie(y, labels=mylabels, colors=mycolors, autopct='%1.1f%%', startangle=90,textprops={'color':'white'})

    plt.title(f'{game_data["name"].iloc[0]} (ID: {game_id})\nVerdeling over de totaal gegeven ratings: {totaal_ratings}', color='white')

    graph_ratings_game = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'graph_ratings_{game_id}.png'))
    plt.savefig(graph_ratings_game)
    #plt.show()
    plt.close()

    return graph_ratings_game

#-------------------------------------------------------------------------------------------------------------------#

df = data_naar_pandas(json_path)
#new_data = kwantitatief_rapportcijfer_pandas(df)
#pandas_naar_json(new_data,'new_steam_data.json')
