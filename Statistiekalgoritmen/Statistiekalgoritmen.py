"""
    Hier gaan wij een lege functie maken met parameters, en de return. Daarbij gaan we ook uitleg
    schrijven over wat de functie doet, waar de parameters voor gebruikt worden,
    en wat de functie uiteindelijk returnt. Alleen dus Statistiekalgoritmen van
    de verplichte onderdelen van Ai.
"""
import pandas as pd
import json

def laad_json_bestand(bestandsnaam):
    """
        Functie beschrijving:
            Deze functie laadt JSON-gegevens uit een bestand of een lijst, en converteert deze naar een Pandas DataFrame.
            Het bestand kan zowel een JSON-bestand als een lijst met JSON-objecten zijn.

        Parameters:
            Bestandsnaam: JSON-bestand of lijst.

        Return:
            Pandas Dataframe.

        Bron:
            - https://saturncloud.io/blog/how-to-convert-nested-json-to-pandas-dataframe-with-specific-format/
            - https://note.nkmk.me/en/python-type-isinstance/
    """

    if type(bestandsnaam) is list:
        data = bestandsnaam
    else:
        with open('steam.json') as bestand:
            data = json.load(bestand)

    #pd.json_normalize convert the JSON to a DataFrame (zie bron)
    df = pd.json_normalize(data,
                           meta=["appid", "name", "name", "english", "developer", "publisher", "platforms",
                                 "required_age", "categories", "genres", "steamspy_tags",
                                 "achievements", "positive_ratings", "negative_ratings", "average_playtime",
                                 "median_playtime", "owners", "price"])
    return df

def laad_eerste_game(df):
    """
        Functie beschrijving:
            Deze functie selecteert de eerste game van een Pandas DataFrame.

        Parameters:
            df: Pandas DataFrame.

        Return:
            Eerste game van de Pandas DataFrame.

        Bron:
            - https://www.statology.org/pandas-select-column-by-index/

    """
    data = df
    return data.iloc[0,:]

def sorteer_data(data,column,ascending_bool,extra_column=None):
    """
        Functie beschrijving:
            Deze functie sorteert data van een Pandas DataFrame obv de meegegeven parameters.

        Parameters:
            - Data: Pandas Dataframe.
            - Column: Kolom waarop gesorteerd wordt.
            - Ascending_bool: Oplopend True/False.
            - Extra_column(optioneel): Kolom waar optioneel op gesorteerd kan worden.

        Return:
            Gesorteerde PandasDataframe

        Bron:
            - https://blog.hubspot.com/website/pandas-sortby#:~:text=Pandas%20Sort%20by%20Column&text=Sorting%20data%20within%20a%20dataframe,the%20values%20in%20descending%20order.
            - https://stackoverflow.com/questions/72098308/how-to-combine-function-with-input-and-except
    """

    if extra_column:
        sorted_df = data.sort_values(by=[column,extra_column], ascending=ascending_bool)
    else:
        sorted_df = data.sort_values(by=(column), ascending=(ascending_bool))

    return sorted_df

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

    lst = []

    for item in data.index:#https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
        positive_reviews = data['positive_ratings'][item]
        negative_reviews = data['negative_ratings'][item]
        game_naam = data['name'][item]
        totaal_ratings = positive_reviews + negative_reviews
        rapportcijfer = (positive_reviews / (totaal_ratings)) * 10  # bijv: 75 / ( 75 + 25) * 10 = 7.5

        game_info = {
            'naam': game_naam,
            'rapportcijfer': round(rapportcijfer, 1),
            'totaal_ratings': totaal_ratings
        }
        lst.append(game_info)
    df = laad_json_bestand(lst)#zet data weer in Panda dataframa

    #https://www.geeksforgeeks.org/how-to-sort-pandas-dataframe/
    return sorteer_data(df,'rapportcijfer',False,'totaal_ratings')#sorteer data op rapportcijfer en op totaal_ratings

data_list = laad_json_bestand('steam2.json')
rapport = (kwantitatief_rapportcijfer_reviews(data_list))
print(rapport[:10])


# ----------------------------------------------------------------------------------------------------------------
# """
#     functie beschrijving:
#         De functie gaat de frequentie berekenen van de genres, om te zien
#         hoevaak elke genre het meest voorkomen in games
#
#     parameters:
#         genres: de genres die worden opgehaald.
#
#     return:
#         De frequentie van elke genre
# """
# def kwatitatief_frequentie_genres(genres):
#     # return genre_frequentie
#
#
#     """
#         functie beschrijving:
#
#
#         parameters:
#
#
#         return:
#     """
# def kwantitatief_frequentie_prijs():
#     # return gemiddelde_review