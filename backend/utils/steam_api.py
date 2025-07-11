import requests

def fetch_steam_user_profile(steam_id, api_key):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    data = response.json()
    return data['response']['players'][0]  # Returns player profile dict