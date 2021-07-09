
# Sparkify ETL Pipeline (Udacity Project 1)

Sparkify seeks to understand "what songs users are listening 
to." This database allows the sparkify team to analyze user 
listening data with simple sql queries, instead of having 
to parse json log files. The repository contains all the 
code needed to create the database and load it with log data.  

## Schema Design

![database schema](/sparkify_db.jpg)

The star schema structure allows the sparkify team 
to gain insights into several key facts including but
not limited to: when certain songs are being played, 
what songs and artist are the most played, what users have 
the most plays. All of this data could help the Sparkify team
target ads and listening experiences better and 
get that :money_with_wings:!

The songplays table is the fact table. This table has the log
of all songplays from all users. There are four dimension 
tables: time, artists, songs, users.

The time table has a parsed time stamp of when a songplay 
occured. This could be useful in getting the amount of times a song was played in a given year. It can be joined to the 
songplays table using the start\_time key. 

The artists table has artist data for each song in it. 
It can be joined to the songplays table using the 
artist\_id key.

The songs table has song data in it. It can be
joined to the songplays table using the song\_id key. It can
also be joined to the artists table using the artist\_id key.

The users table has user data for each song in it. It could 
be used to get the amount of male listeners of a certain song.
It can be joined to the songplays table using the 
user\_id key.

## Example SQL Queries

Get amount of times a song was played  
`SELECT COUNT(*) FROM songplays WHERE song_id='song_id'`

## Installation and Running

### Python Virutal Environment

The ETL pipeline runs in a python virtual environment.
Run `pip install -r requirements.txt` 
to download all dependancies. 

### Docker

A docker container is used for the postgres database that the
ETL script populates. It is set up to run on port 5431.

To build the container run this at the repo's root dir
`docker build -t postgres-student-image .`

To run the container:
`docker run -d --name postgres-student-container -p 5431:5432 
postgres-student-image`

The docker code was adapted from [a project referenced in the project FAQ](https://github.com/kenhanscombe/project-postgres)

Once both docker and the python virtual environment is setup
you can run 
`python create_tables.py` and
`python etl.py`
to create and populate the sparkify database.
