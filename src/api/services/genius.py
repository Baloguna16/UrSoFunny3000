import os
import requests

GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

GENIUS_URL = "https://api.genius.com"

def get_song(song_id=378195):
    credentials = {
        "client_id": GENIUS_CLIENT_ID,
        "client_secret": GENIUS_CLIENT_SECRET,
        "bearer_token": GENIUS_ACCESS_TOKEN
    }

    response = requests.get(f'{GENIUS_URL}/song{song_id}', params=credentials)

    data = response.json
    print(data)
