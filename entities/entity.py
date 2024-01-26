from supabase.client import Client
import os
from spotipy import SpotifyOAuth, Spotify
from dotenv import load_dotenv
class Entity:
    def __init__(self, supabase: Client, table_name: str) -> None:
        load_dotenv()
        self.supabase = supabase
        self.table_name = table_name
        self.SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET") 
        self.SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI")

        self.DATA_LIMIT = 10000
        self.sp = self.refresh()
    
    # Refresh the authorization workflow
    def refresh(self) -> Spotify:
        self.client_credentials_manager = SpotifyOAuth(
            client_id=self.SPOTIFY_CLIENT_ID, client_secret=self.SPOTIFY_CLIENT_SECRET,
            redirect_uri=self.SPOTIFY_REDIRECT_URI,
            scope="user-read-recently-played"
        )
        return Spotify(auth_manager=self.client_credentials_manager)