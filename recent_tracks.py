from supabase import Client
from dotenv import load_dotenv
from spotipy import SpotifyOAuth, Spotify
import os

class RecentTrack:
    def __init__(self, supabase: Client) -> None:
        load_dotenv()
        self.supabase = supabase
        self.SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET") 
        self.SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI")

        self.sp = self.refresh()
    
    # Refresh the authorization workflow
    def refresh(self) -> Spotify:
        self.client_credentials_manager = SpotifyOAuth(
            client_id=self.SPOTIFY_CLIENT_ID, client_secret=self.SPOTIFY_CLIENT_SECRET,
            redirect_uri=self.SPOTIFY_REDIRECT_URI,
            scope="user-read-recently-played"
        )
        return Spotify(auth_manager=self.client_credentials_manager)
    
    def extract(self):
        pass

    def transform(self, entity):
        pass

    def run(self):
        pass