import requests
import datetime

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


def amount_owned_games(key, steamid):
    games = get_json_api(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json",
        "response"
    )
    return games


def all_steam_games(limit=0):
    games = get_json_api("https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json")
    apps = games["applist"]["apps"]
    gamelist = []
    count = 0
    for app in apps:
        if "name" in app and app["name"]:
            gamelist.append({"appid": app["appid"]})
            count += 1
        if count == limit:
            break
    return gamelist


def steam_game_info(gameid):
    game_info = get_json_api(f"https://store.steampowered.com/api/appdetails?appids={gameid}")
    return game_info



def all_owned_games(key, steamid):
    games = get_json_api(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json",
        "response", "games"
    )
    appids = []
    for owned_games_data in games:
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
            all_game_info.append(game_info)
    return all_game_info

def friends_steam_id():
    friends = get_json_api(
        "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid="
        "76561198366424343&relationship=friend",
        "friendslist", "friends"
    )
    friend_list_data = []
    sorted_friends = sorted(friends, key=lambda x: x.get("friend_since"))
    for friend in sorted_friends[:10]:
        steam_id = friend["steamid"]
        friend_list_data.append(steam_id)
    return friend_list_data


def friends_list_info(limit=0):
    friends_list_steam_id = friends_steam_id()
    all_friends_info = []
    for index, steamid in enumerate(friends_list_steam_id[:limit]):
        friend_info = get_json_api(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B129420016573EE260056E21D4218C90&steamids={steamid}",
            "response", "players"
        )
        all_friends_info.append(friend_info)
    return all_friends_info







