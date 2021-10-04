SELECT c_name,
    last_name,
    SUM(amount)
FROM bills
    INNER JOIN customers ON customer_fk = customer_id
    INNER JOIN rents ON rent_id = rent_fk
GROUP BY(customer_id)
HAVING COUNT (customer_id) >= 40