## CSE 6242 HW1 Part 2:
## SQLite
##

import sqlite3
import csv
import json
import pandas as pd


#import CSV files
df_actors = pd.read_csv('Q3_actors.csv', header = None)
df_cast = pd.read_csv('Q3_cast.csv',header = None)
df_movies = pd.read_csv('Q3_movies.csv', header = None)


# create /open a file called hw1part2_sqlite_db, which contains a SQLite db
db = sqlite3.connect('./hw1part2_sqlite_db')
pd.io.sql.write_frame(df_actors, name="actors", con=db)
pd.io.sql.write_frame(df_cast, name="cast", con=db)
pd.io.sql.write_frame(df_movies, name="movies", con=db)

db.execute('BEGIN TRANSACTION')
db.execute('ALTER TABLE actors RENAME TO tmp_actors')
db.execute('''CREATE TABLE actors (id int primary key,name text)''')

db.execute('''INSERT INTO actors(id,name) SELECT 0, 1 from tmp_actors''')
db.execute('COMMIT')


#close the db
db.close()


