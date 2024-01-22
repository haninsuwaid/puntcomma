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

user = get_json_api(
    "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamids=76561198072948436",
    "response", "players")

game = get_json_api(
    "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json", "applist"
)
print(user)
print(game)


# recently_played = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436&format=json"
# owned_games = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436&format=json"
# game_stats = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=HIERGAMENUMMER!&key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436"
# friends = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=4A2585114E9D0E9B541C8CEC0A8D8BAA&steamid=76561198072948436&relationship=friend"
