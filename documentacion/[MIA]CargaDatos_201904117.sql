SELECT DISTINCT (
        nombre_cliente,
        correo_cliente,
        cliente_activo,
        fecha_creacion,
        tienda_preferida,
        direccion_cliente,
        codigo_postal_cliente,
        ciudad_cliente,
        pais_cliente
    )
FROM tempdata
WHERE tempdata.correo_cliente <> '-';

INSERT INTO Customers (
        last_name,
        favorite,
        c_name,
        email,
        active,
        c_date
    )
VALUES (
        '{name[1]}',
        '{row[4]}',
        '{name[0][1:]}',
        '{row[1]}',
        { active },
        '{date}'
    );

SELECT DISTINCT pais_cliente
FROM tempdata
WHERE tempdata.pais_cliente <> '-'
UNION
SELECT DISTINCT pais_empleado
FROM tempdata
WHERE tempdata.pais_empleado <> '-'
UNION
SELECT DISTINCT pais_tienda
FROM tempdata
WHERE tempdata.pais_tienda <> '-';

INSERT INTO Countries
VALUES ('{country}');

SELECT DISTINCT (ciudad_cliente, pais_cliente)
FROM tempdata
WHERE tempdata.pais_cliente <> '-'
    AND tempdata.ciudad_cliente <> '-'
UNION
SELECT DISTINCT (ciudad_empleado, pais_empleado)
FROM tempdata
WHERE tempdata.pais_empleado <> '-'
    AND tempdata.ciudad_empleado <> '-'
UNION
SELECT DISTINCT (ciudad_tienda, pais_tienda)
FROM tempdata
WHERE tempdata.pais_tienda <> '-'
    AND tempdata.ciudad_tienda <> '-';

SELECT DISTINCT (
        direccion_cliente,
        codigo_postal_cliente,
        ciudad_cliente,
        pais_cliente
    )
FROM tempdata
WHERE tempdata.direccion_cliente <> '-'
UNION
SELECT DISTINCT (
        direccion_empleado,
        codigo_postal_empleado,
        ciudad_empleado,
        pais_empleado
    )
FROM tempdata
WHERE tempdata.direccion_empleado <> '-'
UNION
SELECT DISTINCT (
        direccion_tienda,
        codigo_postal_tienda,
        ciudad_tienda,
        pais_tienda
    )
FROM tempdata
WHERE tempdata.direccion_tienda <> '-';

SELECT DISTINCT (direccion_cliente, nombre_cliente)
FROM tempdata
WHERE tempdata.direccion_cliente <> '-'
    AND tempdata.nombre_cliente <> '-';

INSERT INTO CustomerAddress (customer_fk, address_fk)
VALUES (
        (
            SELECT customer_id
            FROM customers
            WHERE customers.c_name = '{name[0]}'
                AND customers.last_name = '{name[1]}'
        ),
        (
            SELECT address_id
            FROM cityaddress
            WHERE cityaddress.address = '{address}'
                AND cityaddress.district = '{district}'
        )
    );

SELECT DISTINCT (nombre_tienda, direccion_tienda)
FROM tempdata
WHERE tempdata.nombre_tienda <> '-'
    AND tempdata.direccion_tienda <> '-';

INSERT INTO Stores (c_name, address, district)
VALUES ('{name}', '{address}', '{district}');

SELECT DISTINCT (
        nombre_empleado,
        correo_empleado,
        empleado_activo,
        tienda_empleado,
        usuario_empleado,
        contrasena_empleado,
        direccion_empleado
    )
FROM tempdata
WHERE tempdata.nombre_empleado <> '-'
    AND tempdata.correo_empleado <> '-';

SELECT DISTINCT (
        nombre_empleado,
        correo_empleado,
        empleado_activo,
        tienda_empleado,
        usuario_empleado,
        contrasena_empleado,
        direccion_empleado
    )
FROM tempdata
WHERE tempdata.nombre_empleado <> '-'
    AND tempdata.correo_empleado <> '-';

SELECT DISTINCT (encargado_tienda, nombre_tienda)
FROM tempdata
WHERE tempdata.encargado_tienda <> '-'
INSERT INTO Bosses (store_fk, employee_fk);

VALUES (
        (
            SELECT store_id
            FROM stores
            WHERE stores.c_name = '{row[1][0:-1]}'
        ),
        (
            SELECT employee_id
            FROM employees
            WHERE employees.c_name = '{name[0]}'
                AND employees.last_name = '{name[1]}'
        )
    );