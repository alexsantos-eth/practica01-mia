SELECT c_name,
    last_name,
    year
FROM movieactors
    INNER JOIN movies ON movie_fk = movie_id
    INNER JOIN actors ON actor_fk = actor_id
WHERE description LIKE '%Crocodile%'
    AND description LIKE '%Shark%'
ORDER BY last_name ASC