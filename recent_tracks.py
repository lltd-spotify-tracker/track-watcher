from supabase import Client
from dotenv import load_dotenv
from spotipy import SpotifyOAuth, Spotify
import os
import time
import logging
from tools import convert_to_unix, convert_to_timestamp

class RecentTrack:
    def __init__(self, supabase: Client, test = False) -> None:
        load_dotenv()
        self.supabase = supabase
        self.SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET") 
        self.SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI")
        self.MAX_RUN_TIME = 24 * 60 * 60 * 1000
        self.test = test

        self.try_extract_time = 0
        self.try_run_time = 0
        now = time.time() * 1000
        self.after_time = int(now - 24*60*60*1000)
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
        self.logger.info('Extracting data at unix time: ' + str(self.after_time))
        try:
            res = self.sp.current_user_recently_played(after=self.after_time)
        except Exception as e:
            self.logger.error("Auth error, refreshing...")
            print(e)
            self.sp = self.refresh()
            res = self.sp.current_user_recently_played(after=self.after_time)
        if not res and self.try_extract_time < 5:
            self.logger.error("No data, retrying...")
            self.try_extract_time += 1
            self.extract()
            return
        self.try_extract_time = 0
        batch_data = []
        tracks = set()

        for item in res.get('items'):
            unix_time = convert_to_unix(item.get('played_at'))
            track_id = item['track']['id']
            tracks.add(track_id)
            batch_data.append (
                {
                    'played_at_unix_time': unix_time,
                    'played_at_utc': item.get('played_at'),
                    'played_at_user_tz': convert_to_timestamp(unix_time),
                    'track_id':item['track']['id'],
                }
            )
            if self.test: break

        for track_id in tracks:
            self.supabase.table('tracks').upsert([
                {
                    'id': track_id
                }
            ]).execute()
        for data in batch_data:
            self.supabase.table('recent_tracks').upsert([
                data
            ]).execute()
        
        self.logger.info('Extracted data at unix time successfully: ' + str(self.after_time))
        self.logger.info('Next: ' + res.get("next", "None"))
        self.after_time = int(res.get('cursors').get('after')) if res.get('cursors') else None

    def run(self):
        print(self.after_time, self.try_run_time, self.MAX_RUN_TIME)
        if not self.after_time or \
            self.try_run_time > self.MAX_RUN_TIME: 
            return

        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler
        log_directory = "logs/recent_tracks"
        os.makedirs(log_directory, exist_ok=True)
        handler = logging.FileHandler(f"{log_directory}/{int(time.time())}.log")

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(handler)

        self.logger.info('Running the extract function time no: ' + str(self.try_run_time))
        self.extract()
        self.try_run_time += 1
        
        # Remove the handler at the end of the function
        self.logger.removeHandler(handler)

        '''TEST'''
        if self.test: exit()
        self.run()
