# Data Warehousing Project
My solution for the data warehousing on AWS project for the Data Engineering Nanodegree on Udacity.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The following steps are tested only for Ubuntu 18.04.

### Amazon Web Services
Place your AWS key and secret into ```data_warehouse/.env``` in the following structure:  
```
AWS_KEY=<your aws key>
AWS_SECRET=<your aws secret>
```
Per default, this file is not synchronized with your remote repository, so your credentials stay on your local machine.

### Virtual Environment
All necessary packages are listed in the ```requirements.txt```file and can be installed by executing:
```
bin/setup
```
This will create a virtual environment ```env``` in your root folder, which you can activate as follows:
```
source env/bin/activate
```

## Running the ETL Process
Running the ETL process is divided in three parts:  
1. Creating the Redshift cluster,
2. Creating the Postgres tables,
3. Populating the tables.  

### Creating the AWS Redshift Cluster
All the code relevant for creating the Redshift cluster, the role and attaching policies can be found in ```data_warehouse/aws.py``` and can be executed as follows:
```
python
from data_warehouse import aws
aws.main()
```
Please mind that executing this script might take approximately 10 minutes, as the program waits for the cluster to be available. Finally, the endpoint and the arn of your cluster will be printed on the screen as follows:
```
DWH_ENDPOINT ::  <your cluster endpoint>
DWH_ROLE_ARN ::  <your cluster arn>
```
This information needs to be added to `data_warehouse/dwh.cfg` as follows:
```
HOST = <your cluster endpoint>
ARN = <your cluster arn>
```

### Creating the Tables
For our data warehouse, one fact table, four dimension tables and two staging tables need to be created.

#### Fact Table
The `songplays` fact table is distributed by `song_id` and sorted by `start_time`.
```
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
```

#### Dimension Table: Artists
The `artists` dimension is relatively small, so that copies can be put on all nodes.
```
CREATE TABLE IF NOT EXISTS artists (
  artist_id VARCHAR PRIMARY KEY,
       name VARCHAR(1024) NOT NULL,
   location VARCHAR(1024),
  lattitude FLOAT,
  longitude FLOAT
)
DISTSTYLE all;
```

#### Dimension Table: Songs
The `songs` dimension is quite big and should be distributed across all nodes. Since songs and artists are usually analyzed jointly, we distribute across `artist_id`.
```
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY,
      title VARCHAR(1024) NOT NULL,
  artist_id VARCHAR NOT NULL REFERENCES artists(artist_id) sortkey distkey,
       year INTEGER,
   duration FLOAT
);
```

#### Dimension Table: Users
There are only few unsers in our table, so we can distribute a copy across all nodes.
Also, there `level` attribute is redundantly placed here and in `songplays`. To track to the change of free and paid level for users, it is advised to use a surrogate key and allow duplicate user_ids. However, this was not pursued in the scope of this project.
```
CREATE TABLE IF NOT EXISTS users (
     user_id INTEGER NOT NULL PRIMARY KEY,
  first_name VARCHAR NOT NULL,
   last_name VARCHAR NOT NULL,
      gender VARCHAR NOT NULL,
       level VARCHAR NOT NULL
)
DISTSTYLE all;
```

#### Dimension Table: Time


```
CREATE TABLE IF NOT EXISTS users (
     user_id INTEGER NOT NULL PRIMARY KEY,
  first_name VARCHAR NOT NULL,
   last_name VARCHAR NOT NULL,
      gender VARCHAR NOT NULL,
       level VARCHAR NOT NULL
)
DISTSTYLE auto;
```

#### Staging Table: Events

```
CREATE TABLE IF NOT EXISTS staging_events (
         artist TEXT,
           auth TEXT,
      firstName TEXT,
         gender TEXT,
  iteminsession INTEGER,
       lastname TEXT,
         length FLOAT,
          level TEXT,
       location TEXT,
         method TEXT,
           page TEXT,
   registration FLOAT,
      sessionid INTEGER,
           song TEXT,
         status INTEGER,
             ts BIGINT,
      useragent TEXT,
         userid FLOAT
);
```

#### Staging Table: Songs

```
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
```

### ETL

#### Copy

##### Staging Events

```
COPY staging_events
FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
FORMAT AS JSON '{}';
```

##### Staging Songs

```
COPY staging_songs
FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
JSON 'auto';
```

#### Insert

##### Artists Dimension

```
INSERT INTO artists
SELECT artist_id,
       artist_name AS name,
       artist_location AS location,
       artist_latitude AS latitude,
       artist_longitude AS longitude
  FROM (SELECT artist_id,
               artist_name,
               artist_location,
               artist_latitude,
               artist_longitude,
               row_number() over (partition by artist_id ORDER BY count desc) AS rn
               FROM (SELECT artist_id,
                            artist_name,
                            artist_location,
                            artist_latitude,
                            artist_longitude,
                            count(*) AS count
                       FROM staging_songs
                      GROUP BY artist_id, artist_name, artist_location, artist_latitude, artist_longitude) AS temp1) AS temp2
 WHERE rn = 1
 ORDER BY artist_id;
```

##### Songs Dimension

```
INSERT INTO songs
SELECT song_id,
       title,
       artist_id,
       year,
       duration
  FROM (SELECT song_id,
               title,
               artist_id,
               year,
               duration,
               row_number() over (partition by song_id ORDER BY count desc) AS rn
               FROM (SELECT song_id,
                            title,
                            artist_id,
                            year,
                            duration,
                            count(*) AS count
                       FROM staging_songs
                      GROUP BY song_id, title, artist_id, year, duration) AS temp1) AS temp2
 WHERE rn = 1
 ORDER BY song_id;
```

##### Time Dimension

```
INSERT INTO time
SELECT start_time,
       date_part(hour, date_time) AS hour,
       date_part(day, date_time) AS day,
       date_part(week, date_time) AS week,
       date_part(month, date_time) AS month,
       date_part(year, date_time) AS year,
       date_part(weekday, date_time) AS weekday
  FROM (SELECT ts AS start_time,
               '1970-01-01'::date + ts/1000 * interval '1 second' AS date_time
          FROM staging_events
         GROUP BY ts) AS temp
 ORDER BY start_time;
```

##### Users Dimension

```
INSERT INTO users
SELECT user_id::INTEGER,
       first_name,
       last_name,
       gender,
       level
  FROM (SELECT userid AS user_id,
               firstname AS first_name,
               lastname AS last_name,
               gender,
               level
          FROM staging_events
         WHERE user_id IS NOT NULL) AS temp
 GROUP BY user_id, first_name, last_name, gender, level
 ORDER BY user_id;
```

##### Songplays Fact

```
INSERT INTO songplays (start_time,
                       user_id,
                       level,
                       song_id,
                       artist_id,
                       session_id,
                       location,
                       user_agent)
SELECT staging_events.ts AS start_time,
       staging_events.userid::INTEGER AS user_id,
       staging_events.level,
       staging_songs.song_id,
       staging_songs.artist_id,
       staging_events.sessionid AS session_id,
       staging_events.location,
       staging_events.useragent AS user_agent
  FROM staging_events
  LEFT join staging_songs
    ON staging_events.song = staging_songs.title
   AND staging_events.artist = staging_songs.artist_name
  LEFT OUTER join songplays
    ON staging_events.userid = songplays.user_id
   AND staging_events.ts = songplays.start_time
 WHERE staging_events.page = 'NextSong'
   AND staging_events.userid IS NOT NULL
   AND staging_events.level IS NOT NULL
   AND staging_songs.song_id IS NOT NULL
   AND staging_songs.artist_id IS NOT NULL
   AND staging_events.sessionid IS NOT NULL
   AND staging_events.location IS NOT NULL
   AND staging_events.useragent IS NOT NULL
   AND songplays.songplay_id is NULL
 ORDER BY start_time, user_id;
```



## Analysis

### Most Popular Artist

![Most Popular Artists](/plots/most_popular_artists.png)

### Most Popular Song

![Most Popular Songs](/plots/most_popular_songs.png)

### Song Plays by Gender and Level

![Song Plays by Gender and Level](/plots/songplays_by_gender_and_level.png)

### Song Plays by Hour

![Song Plays by Hour](/plots/songplays_by_hour.png)
