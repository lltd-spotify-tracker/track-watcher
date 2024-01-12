from dotenv import load_dotenv
import os
import base64
import requests
import json

class SpotifyClient:
    OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    RECENT_TRACK_URL = "https://api.spotify.com/v1/me/player/recently-played"

    def __init__(self) -> None:
        load_dotenv()
        self._client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self._client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token = self.get_token()
    
    def get_token(self):
        auth_string = f"{self._client_id}:{self._client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        headers = {
            "Authorizations": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = { "grant_type": "client_credentials"}
        result = requests.post(self.OAUTH_TOKEN_URL, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result.get("access_token")
        return token

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.token}"}
    
    def get_recent_tracks(self):
        pass