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
        appid = owned_games_data["appid"]
        appids.append(appid)

    return appids

# owned_games_data = all_owned_games()
# print(owned_games_data)


def owned_games_info():
    all_owned_games_ids = all_owned_games()
    for index, appid in enumerate(all_owned_games_ids):
        game_info = get_json_api(
            f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key=B129420016573EE260056E21D4218C90&steamid=76561198366424343",
            "playerstats"
        )
    return game_info


# Call the function
all_owned_games_data = owned_games_info()
print(all_owned_games_data)





# recently_played = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436&format=json"
# owned_games = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436&format=json"
# game_stats = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=HIERGAMENUMMER!&key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436"
# friends = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436&relationship=friend"
