import requests


def get_api_key(data, keys):
    for key in keys:
        data = data.get(key, {})
    return data


def get_json_api(api, *keys):
    response = requests.get(api)

    api_json_data = response.json()
    result = get_api_key(api_json_data, keys)
    return result
def user():
    user = get_json_api(
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B129420016573EE260056E21D4218C90&steamids=76561198366424343",
        "response", "players")
    for data in user:
        persona_name = data["personaname"]
        profile_url = data["profileurl"]
        avatar_full = data["avatarfull"]
        real_name = data["realname"]
        loccountry_code = data["loccountrycode"]
    return data


def all_owned_games():
    games = get_json_api(
        "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=B129420016573EE260056E21D4218C90&steamid=76561198366424343&format=json",
        "response", "games"
    )
    appids = []
    for owned_games_data in games:
        if owned_games_data["playtime_forever"] > 0:
            appid = owned_games_data["appid"]
            appids.append(appid)

    return appids


def owned_games_info(limit=0):
    all_owned_games_ids = all_owned_games()
    all_game_info = []
    for index, appid in enumerate(all_owned_games_ids[:limit]):
        game_info = get_json_api(
            f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key=B129420016573EE260056E21D4218C90&steamid=76561198366424343",
            "playerstats"
        )
        if "gameName" in game_info and game_info["gameName"]:
            all_game_info.append(game_info)
    return all_game_info


def all_steam_games(limit=0):
    games = get_json_api("https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json")
    apps = games["applist"]["apps"]
    gamelist = []
    count = 0
    for app in apps:
        if "name" in app and app["name"]:
            gamelist.append({"appid": app["appid"], "name": app["name"]})
            count += 1
        if count == limit:
            break
    return gamelist


def steam_game_info(gameid):
    game_info = get_json_api(f"https://store.steampowered.com/api/appdetails?appids={gameid}")
    return game_info