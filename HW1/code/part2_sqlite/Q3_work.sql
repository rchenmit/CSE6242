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
select '';

#question 3d
select id,name, year, score from movies where (year>=2011 and year<=2014) order by score desc, name limit 10;
select '';

#question 3e
create table actor_and_count as select actor_id, count(actor_id) count_movies from cast group by actor_id;
select actors.id, actors.name, actor_and_count.count_movies from actors join actor_and_count on actors.id = actor_and_count.actor_id where actor_and_count.count_movies >=10;
select '';

#question 3f
create view movies_score_over_0 as select * from movies where (score>0);
create view cast_in_movies_with_score_over_0 as select `cast`.actor_id actor_id, count(`cast`.actor_id) cnt_movies_with_score_over_0 from `cast` join movies_score_over_0 on `cast`.movie_id = movies_score_over_0.id group by `cast`.actor_id;
create view cast_in_atleast_3_movies_with_score_over_0_tmp as select * from cast_in_movies_with_score_over_0 where cnt_movies_with_score_over_0 >=3;
create view movie_cast_atleast_3_movies_with_score_over_0 as select `cast`.movie_id, `cast`.actor_id from `cast` join cast_in_atleast_3_movies_with_score_over_0_tmp on `cast`.actor_id = cast_in_atleast_3_movies_with_score_over_0_tmp.actor_id;
create view actorid_avgMovieScore_atleast3moviesWithScoreOver0 as select movie_cast_atleast_3_movies_with_score_over_0.actor_id, avg(movies_score_over_0.score) avg_movie_score from movies_score_over_0 join movie_cast_atleast_3_movies_with_score_over_0 on movies_score_over_0.id = movie_cast_atleast_3_movies_with_score_over_0.movie_id group by movie_cast_atleast_3_movies_with_score_over_0.actor_id;
select actorid_avgMovieScore_atleast3moviesWithScoreOver0.actor_id, actors.name, actorid_avgMovieScore_atleast3moviesWithScoreOver0.avg_movie_score from actorid_avgMovieScore_atleast3moviesWithScoreOver0 join actors on actorid_avgMovieScore_atleast3moviesWithScoreOver0.actor_id = actors.id;
select '';

#question 3g
create view cast_list1_movies as select movies.score score, movies.id movie_id, `cast`.actor_id actor_id1 from `cast` join movies on `cast`.movie_id = movies.id;
create view cast_list2_movies as select movies.id movie_id, `cast`.actor_id actor_id2 from `cast` join movies on `cast`.movie_id = movies.id;
create view movie_score_cast_with_two_actorsLists_ALLMOVIES as select cast_list1_movies.score, cast_list1_movies.movie_id, cast_list1_movies.actor_id1, cast_list2_movies.actor_id2 from cast_list1_movies join cast_list2_movies on cast_list1_movies.movie_id = cast_list2_movies.movie_id;
create view actor_collaborations_ALLMOVIES as select actor_id1, actor_id2, avg(score) avg_movie_score, count(score) count_movies from movie_score_cast_with_two_actorsLists_ALLMOVIES where (actor_id1 != actor_id2) group by actor_id1, actor_id2;
create view good_collaboration as select * from actor_collaborations_ALLMOVIES where count_movies >= 2 and avg_movie_score >=75;


#create view actor_collaborations_ALLMOVIES as select actor_id1, actor_id2, avg(score) from movie_score_cast_with_two_actorsLists_ALLMOVIES where actor_id1 != actor_id2 and count(score) >=2 group by actor_id1;


##
select * from movie_score_cast_with_two_actorsLists;



select `cast`.actor_id actor_id1 `cast`.actor_id actor_id2 from `cast` join movies_score_atleast75 on `cast`.movie_id = movies_score_atleast75.id;
create view good_collaboration as select 