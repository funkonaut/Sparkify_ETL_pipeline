import os
import sys

import glob
import logging

import psycopg2
import pandas as pd
from sql_queries import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(stream=sys.stdout)

def process_song_file(cur, filepath):
    """
    Function processes and upserts song data at filepath
    Inserts data into song and artists tables

    Params:
      In: 
        cur->database connection
        filepath->string location of song file
      Out: None    

    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = (
        df[["song_id","title","artist_id","year","duration"]]
        .values
        .tolist()[0]
    )
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (
        df[[
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude"
         ]]
        .values
        .tolist()[0]
    )
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Function processes and upserts log data at filepath.
    Inserts data into timestamp,users,songplays tables.

    Params:
      In: 
        cur->database connection
        filepath->string location of logfile
      Out: None    

    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (
        df['ts'],
        t.dt.hour,
        t.dt.day,
        t.dt.isocalendar().week,
        t.dt.month,
        t.dt.year,
        t.dt.weekday
    )
    column_labels = (
        'timestamp',
        'hour',
        'day',
        'week_of_year',
        'month',
        'year',
        'weekday'
    )
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(
            song_select,
            (row.song, row.artist, row.length)
        )
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent
        )   
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Function gets all files in directory and calls
    process functions to upsert/insert into tables.

    Params:
      In: 
        cur->database connection
        filepath->string location of data directory
        func-> process function to upsert data
      Out: None    

    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Init database connect, do the etl, clean it all up."""
    #database in docker container on port 5431
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb \
         user=student password=student port=5431"
    )
    cur = conn.cursor()

    process_data(
        cur, 
        conn, 
        filepath='data/song_data', 
        func=process_song_file
    )
    process_data(
        cur, 
        conn, 
        filepath='data/log_data', 
        func=process_log_file
    )

    conn.close()


if __name__ == "__main__":
    main()
