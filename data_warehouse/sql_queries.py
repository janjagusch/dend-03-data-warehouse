import configparser
import os

from data_warehouse.config import CONFIG
from data_warehouse.read import read_sql_query


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')


# ROOT PATH
ROOT_PATH = os.path.join(os.path.dirname(__file__), "queries")


# DROP TABLES
staging_events_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "staging_events_table_drop.sql"))
staging_songs_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "staging_songs_table_drop.sql"))
songplay_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "songplay_table_drop.sql"))
user_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "user_table_drop.sql"))
song_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "song_table_drop.sql"))
artist_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "artist_table_drop.sql"))
time_table_drop = read_sql_query(os.path.join(ROOT_PATH, "drop", "time_table_drop.sql"))


# CREATE TABLES
staging_events_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "staging_events_table_create.sql"))
staging_songs_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "staging_songs_table_create.sql"))
songplay_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "songplay_table_create.sql"))
user_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "user_table_create.sql"))
song_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "song_table_create.sql"))
artist_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "artist_table_create.sql"))
time_table_create = read_sql_query(os.path.join(ROOT_PATH, "create", "time_table_create.sql"))


# STAGING TABLES
staging_events_copy = read_sql_query(os.path.join(ROOT_PATH, "copy", "staging_events_copy.sql")).format(CONFIG["S3"]["LOG_DATA"], CONFIG["IAM_ROLE"]["ARN"], CONFIG["S3"]["LOG_JSONPATH"])
staging_songs_copy = read_sql_query(os.path.join(ROOT_PATH, "copy", "staging_songs_copy.sql")).format(CONFIG["S3"]["SONG_DATA"], CONFIG["IAM_ROLE"]["ARN"])


# FINAL TABLES
songplay_table_insert = read_sql_query(os.path.join(ROOT_PATH, "insert", "songplay_table_insert.sql"))
user_table_insert = read_sql_query(os.path.join(ROOT_PATH, "insert", "user_table_insert.sql"))
song_table_insert = read_sql_query(os.path.join(ROOT_PATH, "insert", "song_table_insert.sql"))
artist_table_insert = read_sql_query(os.path.join(ROOT_PATH, "insert", "artist_table_insert.sql"))
time_table_insert = read_sql_query(os.path.join(ROOT_PATH, "insert", "time_table_insert.sql"))


# QUERY LISTS
create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, staging_events_table_create, staging_songs_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, artist_table_insert, song_table_insert, time_table_insert, songplay_table_insert]
