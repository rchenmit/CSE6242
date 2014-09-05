#question 3a
create table movies(id integer primary key, name text, year integer, genre text, score integer);
.separator ","
.import Q3_movies.csv movies
CREATE TABLE movies(id integer primary key, name text, year integer, genre text, score integer);
create table actors(id integer primary key, name text)
.separator ","
.import Q3_actors.csv actors
create table cast (movie_id integer, actor_id integer, character_name text, primary key (movie_id, actor_id));
.separator ","
.import Q3_cast.csv cast
select '';

#question 3b
create index movies_name_index on movies(name);
create index movies_score_index on movies(score);
select '';

#question 3c
select genre, avg(score) from movies where (score>0) group by genre order by genre;

#question 3d
select id,name, year, score from movies where (year>=2011 and year<=2014) order by score desc, name limit 10;

#question 3e