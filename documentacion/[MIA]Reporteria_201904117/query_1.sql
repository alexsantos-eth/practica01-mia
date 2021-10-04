SELECT COUNT(movie_fk)
FROM stocks
    INNER JOIN movies ON movie_fk = movie_id
WHERE movies.title = 'SUGAR WONKA'
GROUP BY movie_fk