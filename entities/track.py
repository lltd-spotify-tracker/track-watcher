from supabase.client import Client
from entity import Entity

class Track(Entity):
    def __init__(self, supabase: Client) -> None:
        super().__init__(supabase, table_name="tracks")
        self.max_iter = 1000
    
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
                .execute().limit(10000)
            if not query: return
            for track in query[1]:
                track_obj = self.sp.track(track.get("id"))

                track_data = {
                    "id": track_obj["id"],
                    "name": track_obj["name"],
                    "spotify_url": track_obj.get("external_urls")\
                        .get("spotify") if track_obj.get("external_urls") else None,
                    "duration_ms": track_obj["duration_ms"]
                }

                self.upsert(data=track_data)

                for artist in track_obj["artists"]:
                    tracks_artists_data = {
                        "track_id": track_obj["id"],
                        "artist_id": artist["id"]
                    }
                    self.upsert(table_name="tracks_artists", data=[tracks_artists_data])

                    artist_data = {
                        "id": artist["id"],
                        "name": artist["name"],
                        "spotify_url": artist.get("external_urls").get("spotify") if artist.get("external_urls") else None
                    }
                    self.upsert(table_name="artists", data=[artist_data])

                album = track_obj.get("album")
                if album:
                    album_data = {
                        "id": album["id"],
                        "name": album["name"],
                        "spotify_url": album.get("external_urls").get("spotify") if album.get("external_urls") else None,
                    }
                    self.upsert(table_name="albums", data=[album_data])