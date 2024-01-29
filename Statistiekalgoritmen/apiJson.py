import requests
import datetime
import random

def get_api_key(data, keys):
    for key in keys:
        data = data.get(key, {})
    return data


def get_json_api(api, *keys):
    response = requests.get(api)
    api_json_data = response.json()
    result = get_api_key(api_json_data, keys)
    return result

def user(key, steamid):
    user = get_json_api(
        f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}",
        "response", "players")

    return user

def user_by_id(key, steamid):
    user = get_json_api(
        f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}",
        "response", "players")

    return user

def amount_owned_games(key, steamid):
    games = get_json_api(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json",
        "response"
    )
    return games


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


def all_owned_games(key, steamid):
    games = get_json_api(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json",
        "response", "games"
    )
    appids = []
    sorted_games = sorted(games, key=lambda x: x.get("playtime_forever"))
    for owned_games_data in sorted_games:
        if owned_games_data["playtime_forever"] > 0:
            appid = owned_games_data["appid"]
            appids.append(appid)
    return appids


def owned_games_info(key, steamid, limit=0):
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
    friends = get_json_api(
        f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamid}&relationship=friend",
        "friendslist", "friends"
    )
    friend_list_data = []
    sorted_friends = sorted(friends, key=lambda x: x.get("friend_since"))
    for friend in sorted_friends[:10]:
        steam_id = friend["steamid"]
        friend_list_data.append(steam_id)
    return friend_list_data


def friends_list_info(key, steamid, limit=0):
    friends_list_steam_id = friends_steam_id(key, steamid)
    all_friends_info = []
    for index, steamid in enumerate(friends_list_steam_id[:limit]):
        friend_info = get_json_api(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}",
            "response", "players"
        )
        all_friends_info.append(friend_info)
    return all_friends_info







