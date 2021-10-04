DROP TABLE IF EXISTS temp_bills;

CREATE TEMPORARY TABLE temp_bills AS (
    SELECT country_id AS cs,
        COUNT(movie_id) AS sport_counts
    FROM bills
        INNER JOIN movies ON bills.movie_fk = movies.movie_id
        INNER JOIN customeraddress ON bills.customer_fk = customeraddress.customer_fk
        INNER JOIN cityaddress ON address_fk = address_id
        INNER JOIN cities ON city_fk = city_id
        INNER JOIN countries ON country_fk = country_id
        INNER JOIN MovieCategories ON MovieCategories.movie_fk = movies.movie_id
    WHERE category_fk = 'Sports'
    GROUP BY country_id
);

DROP TABLE IF EXISTS temp_rents;

CREATE TEMPORARY TABLE temp_rents AS (
    SELECT country_id AS cs,
        COUNT(bill_id) AS rent_counts
    FROM bills
        INNER JOIN customeraddress ON bills.customer_fk = customeraddress.customer_fk
        INNER JOIN cityaddress ON address_fk = address_id
        INNER JOIN cities ON city_fk = city_id
        INNER JOIN countries ON country_fk = country_id
    GROUP BY country_id
);

SELECT temp_rents.cs,
    concat(
        trunc(
            (
                cast(temp_bills.sport_counts AS decimal(10, 2)) / cast(temp_rents.rent_counts AS decimal(10, 2))
            ) * 100,
            2
        ),
        '%'
    )
FROM temp_rents
    INNER JOIN temp_bills ON temp_rents.cs = temp_bills.cs;