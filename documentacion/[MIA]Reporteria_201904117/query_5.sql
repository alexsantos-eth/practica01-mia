SELECT c.c_name,
    c.last_name,
    p.country_id,
    COUNT(R.customer_fk),
    (COUNT (R.customer_fk) * 100) /(
        SELECT COUNT(R.customer_fk)
        FROM bills R
            INNER JOIN customers c ON c.customer_id = r.customer_fk
            INNER JOIN customeraddress d ON d.customer_fk = c.customer_id
            INNER JOIN cityaddress f ON f.address_id = d.address_fk
            INNER JOIN cities q ON q.city_id = f.city_fk
            INNER JOIN countries z ON z.country_id = q.country_fk
        WHERE z.country_id = p.country_id
        GROUP BY z.country_id
    )
FROM bills R
    INNER JOIN customers c ON c.customer_id = r.customer_fk
    INNER JOIN customeraddress d ON d.customer_fk = c.customer_id
    INNER JOIN cityaddress f ON f.address_id = d.address_fk
    INNER JOIN cities q ON q.city_id = f.city_fk
    INNER JOIN countries p ON p.country_id = q.country_fk
GROUP BY c.c_name,
    c.last_name,
    p.country_id
ORDER BY COUNT(R.customer_fk) DESC
LIMIT 1;