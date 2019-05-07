CREATE TABLE IF NOT EXISTS songplays (
  songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
   start_time BIGINT NOT NULL REFERENCES time(start_time) sortkey,
      user_id INTEGER NOT NULL REFERENCES users(user_id),
        level VARCHAR NOT NULL,
      song_id VARCHAR NOT NULL REFERENCES songs(song_id) distkey,
    artist_id VARCHAR NOT NULL REFERENCES artists(artist_id),
   session_id INTEGER NOT NULL,
     location VARCHAR NOT NULL,
   user_agent VARCHAR NOT NULL
);
