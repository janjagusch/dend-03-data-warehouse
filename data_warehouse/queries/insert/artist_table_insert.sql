insert into artists
select artist_id,
       artist_name as name,
       artist_location as location,
       artist_latitude as latitude,
       artist_longitude as longitude
  from (select artist_id,
               artist_name,
               artist_location,
               artist_latitude,
               artist_longitude,
               row_number() over (partition by artist_id order by count desc) as rn
               from (select artist_id,
                            artist_name,
                            artist_location,
                            artist_latitude,
                            artist_longitude,
                            count(*) as count
                       from staging_songs
                      group by artist_id, artist_name, artist_location, artist_latitude, artist_longitude) as temp1) as temp2
 where rn = 1
 order by artist_id;
