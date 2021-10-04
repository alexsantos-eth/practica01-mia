SELECT cities.city_name,
    COUNT(bills.customer_fk)
FROM bills,
    customeraddress,
    cityaddress,
    cities,
    countries
WHERE bills.customer_fk = customeraddress.customer_fk
    AND customeraddress.address_fk = cityaddress.address_id
    AND cityaddress.city_fk = cities.city_id
    AND cities.country_fk = countries.country_id
    AND countries.country_id = 'United States'
GROUP BY cities.city_name
HAVING COUNT(bills.customer_fk) > (
        SELECT COUNT(bills.customer_fk)
        FROM bills,
            customeraddress,
            cityaddress,
            cities,
            countries
        WHERE bills.customer_fk = customeraddress.customer_fk
            AND customeraddress.address_fk = cityaddress.address_id
            AND cityaddress.city_fk = cities.city_id
            AND cities.country_fk = countries.country_id
            AND countries.country_id = 'United States'
            AND cities.city_name = 'Dayton'
    )
ORDER BY cities.city_name