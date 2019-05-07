CREATE TABLE IF NOT EXISTS time (
  start_time BIGINT PRIMARY KEY,
        hour INTEGER,
         day INTEGER,
        week INTEGER,
       month INTEGER,
        year INTEGER distkey,
     weekday INTEGER
)
DISTSTYLE auto;
