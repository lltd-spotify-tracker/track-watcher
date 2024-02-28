from entities.entity import Entity
from supabase.client import Client

sql = '''
select
  rt.user_id,
  to_char(rt.played_at_user_tz::date, 'YYYY-MM-DD') as date_id,
  rt.played_at_user_tz::date as date,
  sum(t.duration_ms)::integer as total
from
  recent_tracks rt
  join tracks t on rt.track_id = t.id
group by
  rt.user_id,
  rt.played_at_user_tz::date;
'''

class DailyListeningHour (Entity):
    def __init__(self, supabase: Client) -> None:
        super().__init__(supabase, table_name="daily_listening_hour")
        self.max_iter = 1000
    