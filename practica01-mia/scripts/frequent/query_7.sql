DROP TABLE IF EXISTS temp_data;

CREATE TEMPORARY TABLE temp_data AS (
    SELECT country_id AS cs,
        COUNT(bill_id) AS counts
    FROM bills
        INNER JOIN customeraddress ON bills.customer_fk = customeraddress.customer_fk
        INNER JOIN cityaddress ON address_fk = address_id
        INNER JOIN cities ON city_fk = city_id
        INNER JOIN countries ON country_fk = country_id
    GROUP BY country_id
);

SELECT country_id AS country,
    cities.city_name,
    concat(
        trunc(
            cast(COUNT(bill_id) AS decimal(10, 2)) / cast(
                (
                    SELECT counts
                    FROM temp_data
                    WHERE temp_data.cs = country_id
                ) AS decimal(10, 2)
            ) * 100,
            2
        ),
        '%'
    ),
    (
        SELECT counts
        FROM temp_data
        WHERE temp_data.cs = country_id
    )
FROM bills
    INNER JOIN customeraddress ON bills.customer_fk = customeraddress.customer_fk
    INNER JOIN cityaddress ON address_fk = address_id
    INNER JOIN cities ON city_fk = city_id
    INNER JOIN countries ON country_fk = country_id
GROUP BY country,
    cities.city_name;