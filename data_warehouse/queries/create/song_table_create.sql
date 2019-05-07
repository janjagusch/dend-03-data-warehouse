CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY,
      title VARCHAR(1024) NOT NULL,
  artist_id VARCHAR NOT NULL REFERENCES artists(artist_id) sortkey distkey,
       year INTEGER,
   duration FLOAT
);
