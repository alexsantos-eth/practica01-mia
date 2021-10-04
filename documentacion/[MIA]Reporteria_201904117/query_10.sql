DROP TABLE IF EXISTS temp_rents;

CREATE TEMPORARY TABLE temp_rents AS (
    SELECT country_id,
        city_name,
        MovieCategories.category_fk,
        COUNT (MovieCategories.category_fk) AS counts
    FROM bills
        INNER JOIN movies ON bills.movie_fk = movies.movie_id
        INNER JOIN customeraddress ON bills.customer_fk = customeraddress.customer_fk
        INNER JOIN cityaddress ON address_fk = address_id
        INNER JOIN cities ON city_fk = city_id
        INNER JOIN countries ON country_fk = country_id
        INNER JOIN MovieCategories ON MovieCategories.movie_fk = movies.movie_id
    GROUP BY (
            country_id,
            city_name,
            MovieCategories.category_fk
        )
);

DROP TABLE IF EXISTS temp_max;

CREATE TEMPORARY TABLE temp_max AS (
    SELECT country_id,
        city_name,
        max(counts)
    FROM temp_rents
    GROUP BY country_id,
        city_name
);

SELECT temp_max.country_id,
    temp_max.city_name
FROM temp_rents
    INNER JOIN temp_max ON temp_max.country_id = temp_rents.country_id
    AND temp_max.city_name = temp_rents.city_name
    AND temp_max.max = temp_rents.counts
WHERE category_fk = 'Horror';