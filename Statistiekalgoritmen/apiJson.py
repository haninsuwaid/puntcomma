import requests
import random
import asyncio
from basisfuncties.basisfuncties import *


def get_api_key(data, keys):
    """
        Functie beschrijving:
            loop to access nested keys
        Parameters:
            data: for the api link
            keys: for the keys of the api
        Return:
            data: the last key or if not found an empty dict
    """
    for key in keys:
        data = data.get(key, {})
    return data


def get_json_api(api, *keys):
    """
        Functie beschrijving:
            this function is to make api calls
        Parameters:
            api: the api call link
            *keys: the keys of the api call the * means it could have multiple keys
        Return:
            result: the whole api call with the link and the key/s needed
    """
    response = requests.get(api)
    api_json_data = response.json()
    result = get_api_key(api_json_data, keys)
    return result


def all_steam_games(limit=0):
    """
        function description:
            This function returns a chosen amount of random steam games based on the parameter

        parameters:
            limit: The number of games it will get from the api

        return: gamelist
    """
    # Get the games out of the api
    games = get_json_api("https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json")
    apps = games["applist"]["apps"]
    # Shuffles the games in a random order
    random.shuffle(apps)
    gamelist = []
    count = 0
    # Uses for statement to loop through all the games
    for app in apps:
        # Only add games that have a name
        if "name" in app and app["name"]:
            # Append the appid to the empty array
            gamelist.append({"appid": app["appid"]})
            count += 1
        # if the count is equal to the parameter it will break the function and return the gamelist
        if count == limit:
            break
    return gamelist


def steam_game_info(gameid):
    """
        function description:
            This function returns information of the chosen steam game

        parameters:
            gameid: The id that chooses which games information will be shown

        return: game_info
    """
    game_info = get_json_api(f"https://store.steampowered.com/api/appdetails?appids={gameid}")
    return game_info


def info_for_steam_games():
    """
        function description:
            This function will return a list of steam games with the information of the games

        return: game_info_steam
    """

    # Calls the function "all_steam_games" that returns all the ids from games and puts it in "list_of_games"
    list_of_games = all_steam_games(limit=10)
    # Loops through each id in the list_of_games. Call the function steam_game_info with the appid,
    # To get all the data from the random chosen steam game, put it in a var and return the game_inf_steam
    game_info_steam = [steam_game_info(game["appid"]) for game in list_of_games]
    return game_info_steam


# async def nested():
#     return 42
#
#
# async def main():
#     await asyncio.gather(nested())
#
# asyncio.run(main())


def user(key, steamid):
    """
        Functie beschrijving:
            Api to get player's info with their key and steamid
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
        Return:
            dataset of users data
    """
    user = get_json_api(
        f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}",
        "response", "players")
    return user


def user_by_id(key, steamid):
    """
        Functie beschrijving:
            this function get the users id
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
        Return:
            user's id
    """
    user_id = get_json_api(
        f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}",
        "response", "players")

    return user_id



def amount_owned_games(key, steamid):
    """
        Functie beschrijving:
            this function gets the amout of owned games from owned games api it get the first key.
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
        Return:
            the key where the amount of games the user has is mentioned
    """
    games = get_json_api(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json",
        "response"
    )
    return games


def all_owned_games(key, steamid):
    """
        Functie beschrijving:
            this function gets all owned games of the logged-in user and the appids. And it sorts games
            based of the playtime. From most played to least played
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
        Return:
            it returns the appids of the owned games if the playtime is larger then 0
    """
    games = get_json_api(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json",
        "response", "games"
    )
    appids = []
    df = (data_naar_pandas(games))
    df_sorteer_games = sorteer_data(df,"playtime_forever", False)
    for app_id in df_sorteer_games['appid']:
        appids.append(app_id)
    return appids


def owned_games_info(key, steamid, limit=0):
    """
        Functie beschrijving:
            this function get the all_owned_games function that has all appids of owned games with playtime
            it limits the amount of games I want to get. It also checks if the key gamename exists and is not empty
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
            limit=0:
        Return:
            games info with gameName
    """
    all_owned_games_ids = all_owned_games(key, steamid)
    all_game_info = []
    for index, appid in enumerate(all_owned_games_ids[:limit]):
        game_info = get_json_api(
            f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={key}&steamid={steamid}",
            "playerstats"
        )
        if "gameName" in game_info and game_info["gameName"]:
            all_game_info.append({"appid": appid, "game_info": game_info})
    return all_game_info


def friends_steam_id(key, steamid):
    """
        Functie beschrijving:
            this function gets friends steam id to use the id in another function where i get their data
            with the steamids. This function sorts friends from the oldest to newest friends.
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
        Return:
            a list of steamids
    """
    friends = get_json_api(
        f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamid}&relationship=friend",
        "friendslist", "friends"
    )
    steamid_oldst_friends = []
    df = (data_naar_pandas(friends))
    df_sorteer = sorteer_data(df, 'friend_since', True)
    for steamid in df_sorteer['steamid']:
        steamid_oldst_friends.append(steamid)
    return steamid_oldst_friends


def friends_list_info(key, steamid, limit=0):
    """
        Functie beschrijving:
            a function to get the steam ids from the another function and get the data of the friends.
        Parameters:
            key: the key the user gets from steam to get their own api link
            steamid: the steamid the user gets from using steam
            limit=0: a limit to limit the amout of friends i want to get
        Return:
            a list of friends info
    """
    friends_list_steam_id = friends_steam_id(key, steamid)
    all_friends_info = []
    for index, steamid in enumerate(friends_list_steam_id[:limit]):
        friend_info = get_json_api(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}",
            "response", "players"
        )
        all_friends_info.append(friend_info)
    return all_friends_info