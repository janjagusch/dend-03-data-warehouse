CREATE TABLE IF NOT EXISTS staging_songs (
           song_id TEXT PRIMARY KEY,
             title VARCHAR(1024),
          duration FLOAT,
              year FLOAT,
         num_songs FLOAT,
         artist_id TEXT,
       artist_name VARCHAR(1024),
   artist_latitude FLOAT,
  artist_longitude FLOAT,
   artist_location VARCHAR(1024)
);
