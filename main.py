from dotenv import load_dotenv
from supabase import create_client
from recent_tracks import RecentTrack
import os


if __name__ == "__main__":
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase = create_client(supabase_url, supabase_key)
    recent_track = RecentTrack(supabase)
    recent_track.run()
