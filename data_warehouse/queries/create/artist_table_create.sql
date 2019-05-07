CREATE TABLE IF NOT EXISTS artists (
  artist_id VARCHAR PRIMARY KEY,
       name VARCHAR(1024) NOT NULL,
   location VARCHAR(1024),
  lattitude FLOAT,
  longitude FLOAT
)
DISTSTYLE all;
