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
All necessary packages are listed in the ```requirements.txt```file and can be intalled by executing:
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

#### Staging Table: Songs

### ETL

## Analysis

![Most Popular Artists](/plots/most_popular_artists.png)

![Most Popular Songs](/plots/most_popular_songs.png)

![Song Plays by Gender and Level](/plots/songplays_by_gender_and_level.png)

![Song Plays by Hour](/plots/songplays_by_hour.png)
