import pandas as pd
import json
import os


def data_naar_pandas(JsonOrLst):
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
            - https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
    """

    if type(JsonOrLst) is list:
        data = JsonOrLst
        df = pd.DataFrame(data)
    else:
        with open((JsonOrLst)) as bestand:
            data = json.load(bestand)

            # pd.json_normalize convert the JSON to a DataFrame (zie bron)
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

def pandas_naar_json(df, filename):
    """
        Functie beschrijving:
            Deze functie converteerd een Pandas Dataframe naar een lijst met dicts en
            schrijft deze vervolgens weg naar een .json bestand.

        Parameters:
            - Data: Pandas Dataframe.
            - Filename: Naam waar het bestand naar genoemd dient te worden.

        Return:
            .json bestand

        Bron:
            - https://datatofish.com/export-pandas-dataframe-json/
    """
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','puntcomma', 'json', filename))
    json_list = df.to_dict(orient='records') #(zie bron) zet panda dataframe om naar een lijst met dicts
    with open(f'{json_path}', 'x') as bestand:
        json.dump(json_list, bestand, indent=4)

#-------------------------------------------------------------------------------------------------------------------#
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'json', 'new_steam.json'))
