insert into songplays (start_time,
                       user_id,
                       level,
                       song_id,
                       artist_id,
                       session_id,
                       location,
                       user_agent)
select staging_events.ts as start_time,
       staging_events.userid::INTEGER as user_id,
       staging_events.level,
       staging_songs.song_id,
       staging_songs.artist_id,
       staging_events.sessionid as session_id,
       staging_events.location,
       staging_events.useragent as user_agent
  from staging_events
  left join staging_songs
    on staging_events.song = staging_songs.title
   and staging_events.artist = staging_songs.artist_name
  left outer join songplays
    on staging_events.userid = songplays.user_id
   and staging_events.ts = songplays.start_time
 where staging_events.page = 'NextSong'
   and staging_events.userid is not Null
   and staging_events.level is not Null
   and staging_songs.song_id is not Null
   and staging_songs.artist_id is not Null
   and staging_events.sessionid is not Null
   and staging_events.location is not Null
   and staging_events.useragent is not Null
   and songplays.songplay_id is Null
 order by start_time, user_id
;
