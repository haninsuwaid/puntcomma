from basisfuncties import *

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

    return sorteer_data(data, 'cijfer', False)

def plot_histogram_rapportcijfers(data):
    """
        Functie beschrijving:
            Deze functie visualiseert het aantal games per bijbehorend rapportcijfer in de vorm van een histogram.

        Parameters:
            Data: Pandas dataframe.

        Return:
            Histogram.
    """
    #Afmetingen figuur
    plt.figure(figsize=(10, 10))
    plt.figure(facecolor='#1b2838')

    #Maak Historgram
    plt.hist(data['cijfer'], bins=20, color='#354f52', alpha=1, edgecolor='white')


    #x,y,titelnaam
    plt.xlabel('Rapportcijfer', color ="white")
    plt.ylabel('Aantal Games', color="white")
    plt.title('Rapportcijfers', color="white")
    plt.yticks(color="white")
    plt.xticks(color="white")

    plt.xticks(np.arange(0, 10.5))

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

    # Save the figure
    graph_ratings_game = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'graph_ratings_{game_id}.png'))
    plt.savefig(graph_ratings_game)

    # Close the plot to free up resources
    plt.close()

    return graph_ratings_game


#--------------------------------------------------------------------------------------------------------------------------------#
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'json', 'steam.json'))

df = laad_json_bestand(json_path)
new_data = kwantitatief_rapportcijfer_reviews(df)

#from_pandas_to_json(new_data,'new_steam_data.json')

plot_histogram_rapportcijfers(new_data)
plot_insight_ratings_per_game(new_data,20)
