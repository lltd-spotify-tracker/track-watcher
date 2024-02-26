from supabase.client import Client
from .entity import Entity

class Track(Entity):
    def __init__(self, supabase: Client) -> None:
        super().__init__(supabase, table_name="tracks")
        self.max_iter = 1000
    
    def extract_genres(self, album_id: str, genres: list):
        # Extract the genres from the album
        album_detail = self.sp.album(album_id)
        genres = set(album_detail.get("genres"))
        label = album_detail.get("label")
        if 'lofi' in label.lower(): genres.add("lofi")
        for genre in genres:
            genre_data = {
                'name': genre.lower()
            }
            self.supabase.table("genres")\
                .upsert(genre_data).execute()
            albums_genres_data = {
                "album_id": album_id,
                "genre": genre.lower()
            }
            self.supabase.table("albums_genres")\
                .upsert(albums_genres_data).execute()
    
    def etl(self):
        etl_iter = 0
        while etl_iter < self.max_iter:
            etl_iter += 1
            query, _ = self.supabase.table("tracks")\
                .select("*")\
                .is_("album_id", 'null')\
                .is_("name", 'null')\
                .is_("spotify_url", 'null')\
                .eq("duration_ms", 0)\
                .limit(self.DATA_LIMIT)\
                .execute()
            if not query[1]: return
            for track in query[1]:
                track_obj = self.sp.track(track.get("id"))

                album = track_obj.get("album")
                if album:
                    album_data = {
                        "id": album["id"],
                        "name": album["name"],
                        "spotify_url": album.get("external_urls").get("spotify") if album.get("external_urls") else None,
                    }
                    self.supabase.table("albums")\
                        .upsert(album_data).execute()

                track_data = {
                    "id": track_obj["id"],
                    "name": track_obj["name"],
                    "spotify_url": track_obj.get("external_urls")\
                        .get("spotify") if track_obj.get("external_urls") else None,
                    "duration_ms": track_obj["duration_ms"],
                    'album_id': album["id"] if album else None,
                }

                self.supabase.table(self.table_name)\
                    .upsert(track_data).execute()

                for artist in track_obj["artists"]:
                    tracks_artists_data = {
                        "track_id": track_obj["id"],
                        "artist_id": artist["id"]
                    }

                    artist_data = {
                        "id": artist["id"],
                        "name": artist["name"],
                        "spotify_url": artist.get("external_urls").get("spotify") if artist.get("external_urls") else None
                    }
                    self.supabase.table("artists")\
                        .upsert(artist_data).execute()
                    self.supabase.table("tracks_artists")\
                        .upsert(tracks_artists_data).execute()

                