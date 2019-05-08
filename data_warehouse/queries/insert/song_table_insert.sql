insert into songs
select song_id,
       title,
       artist_id,
       year,
       duration
  from (select song_id,
               title,
               artist_id,
               year,
               duration,
               row_number() over (partition by song_id order by count desc) as rn
               from (select song_id,
                            title,
                            artist_id,
                            year,
                            duration,
                            count(*) as count
                       from staging_songs
                      group by song_id, title, artist_id, year, duration) as temp1) as temp2
 where rn = 1
 order by song_id;
