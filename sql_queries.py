"""
Queries to create and drop tables in db:

FACT TABLE:
songplays - records in log data associated with song plays 
i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, 
session_id, location, user_agent

DIMENSION TABLES:
users - users in the app
user_id, first_name, last_name, gender, level

songs - songs in music database
song_id, title, artist_id, year, duration

artists - artists in music database
artist_id, name, location, latitude, longitude

time - timestamps of records in songplays broken down into 
specific units
start_time, hour, day, week, month, year, weekday

"""

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
songplay_table_create = (
    """CREATE TABLE IF NOT EXISTS songplays(
         songplay_id BIGSERIAL PRIMARY KEY,
         start_time BIGINT NOT NULL, 
         user_id INT NOT NULL, 
         level text, 
         song_id TEXT, 
         artist_id TEXT, 
         session_id INT, 
         location TEXT, 
         user_agent TEXT,
         CONSTRAINT fk_start_time
           FOREIGN KEY (start_time)
             REFERENCES time(start_time),
         CONSTRAINT fk_user_id
           FOREIGN KEY (user_id)
             REFERENCES users(user_id),
         CONSTRAINT fk_song_id
           FOREIGN KEY (song_id)
             REFERENCES songs(song_id),
         CONSTRAINT fk_artist_id
           FOREIGN KEY (artist_id)
             REFERENCES artists(artist_id));
    """
)

user_table_create = (
    """CREATE TABLE IF NOT EXISTS users(
         user_id BIGINT PRIMARY KEY, 
         first_name TEXT, 
         last_name TEXT, 
         gender TEXT, 
         level TEXT);
    """
)
#should i add fk constraint on atist_id or not null
song_table_create = (
    """CREATE TABLE IF NOT EXISTS songs(
         song_id TEXT PRIMARY KEY, 
         title TEXT, 
         artist_id TEXT, 
         year INT, 
         duration NUMERIC); 
    """
)

artist_table_create = (
    """CREATE TABLE IF NOT EXISTS artists(
         artist_id TEXT PRIMARY KEY, 
         name TEXT, 
         location TEXT, 
         latitude NUMERIC, 
         longitude NUMERIC);
    """
)

time_table_create = (
    """CREATE TABLE IF NOT EXISTS time(
         start_time BIGINT PRIMARY KEY, 
         hour INT,
         day INT,
         week INT, 
         month INT, 
         year INT, 
         weekday INT);
    """
)

# INSERT RECORDS

songplay_table_insert = (
    """
    INSERT INTO songplays(
         start_time, 
         user_id, 
         level, 
         song_id, 
         artist_id, 
         session_id, 
         location, 
         user_agent)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s);
    """
)

user_table_insert = (
    """
    INSERT INTO users(
      user_id,
      first_name,
      last_name,
      gender,
      level)
    VALUES(%s,%s,%s,%s,%s)
    ON CONFLICT (user_id)
    DO
      UPDATE SET
        first_name=excluded.first_name,
        last_name=excluded.last_name,
        gender=excluded.gender,
        level=excluded.level;
    """
)

song_table_insert = (
    """
    INSERT INTO songs(
      song_id, 
      title, 
      artist_id, 
      year, 
      duration)
    VALUES(%s,%s,%s,%s,%s)
    ON CONFLICT (song_id)
    DO 
      UPDATE SET
        title=excluded.title,
        artist_id=excluded.artist_id,
        year=excluded.year,
        duration=excluded.duration;
    """
)


artist_table_insert = (
    """
    INSERT INTO artists(
      artist_id, 
      name, 
      location, 
      latitude, 
      longitude)
    VALUES(%s,%s,%s,%s,%s)
    ON CONFLICT (artist_id)
    DO 
      UPDATE SET
        name=excluded.name,
        location=excluded.location,
        latitude=excluded.latitude,
        longitude=excluded.longitude
    """
)

time_table_insert = (
    """
    INSERT INTO time(
      start_time, 
      hour, 
      day, 
      week, 
      month, 
      year, 
      weekday)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time)
    DO NOTHING;
    """
)

# FIND SONGS
#song ID and artist ID based on the title, artist name, and duration of a song.
song_select = (
    """
    SELECT 
      songs.song_id, 
      songs.artist_id
    FROM songs
    JOIN artists ON
       songs.artist_id = artists.artist_id
    WHERE 
      songs.title = %s AND
      artists.name = %s AND
      songs.duration = %s;
    """
)

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
