from dotenv import load_dotenv
from supabase import create_client
from recent_tracks import RecentTrack
import os
import argparse

HELPER_STRING = {
    "options": '''
    The option to run:
    - recent_track or r: Extract the recent tracks from Spotify and store them in the database
    '''
}

if __name__ == "__main__":
    # Create a parser
    parser = argparse.ArgumentParser()

    # Add the 'options' argument
    parser.add_argument('--options', '-o', type=str, help=HELPER_STRING['options'])

    # Parse the arguments
    args = parser.parse_args()

    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase = create_client(supabase_url, supabase_key)

    # Check if the 'options' argument is 'recent_track'
    if args.options == 'recent_track' or args.options == 'r':
        recent_track = RecentTrack(supabase)
        recent_track.run()