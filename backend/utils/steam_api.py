import requests

def fetch_steam_user_profile(steam_id, api_key):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    data = response.json()
    return data['response']['players'][0]  # Returns player profile dict

def fetch_steam_owned_games(steam_id, api_key):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&include_appinfo=true"
    response = requests.get(url)
    data = response.json()
    return data.get('response', {}).get('games', [])