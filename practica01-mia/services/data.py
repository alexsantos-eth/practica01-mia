from api.utils import Service
from flask import jsonify
from csv import reader
import os


class data_service(Service):
    # EJECUTAR SCRIPT
    def exectue_psql(self, path, commit=True):
        sql_file = os.path.join(os.path.dirname(
            __file__), f'../scripts/{path}.sql')
        with open(sql_file, 'r', encoding='utf8') as file:
            self.cursor.execute(file.read())
            if commit:
                self.connect.commit()

    # SUBIR ARCHIVO CSV
    def upload_temporal(self):
        self.exectue_psql('upload')
        return "CSV Cargado correctamente"

    # FECHA A TIMESTAMP
    def date_to_timestamp(self, date_str):
        date_s = date_str.split(' ')
        date_d = date_s[0].split('/')
        date = f'{date_d[2]}-{date_d[1]}-{date_d[0]} {date_s[1]}:00'
        return date

    # CREAR MODELO CON TABLA TEMPORAL
    def set_data_model(self):
        # CREAR CLIENTES
        self.cursor.execute("""
        CREATE TABLE Customers (
            customer_id SERIAL PRIMARY KEY,
            last_name VARCHAR(250),
            favorite VARCHAR(250),
            c_name VARCHAR(250),
            email VARCHAR(250),
            active BOOLEAN,
            c_date DATE
        );""")

        # OBTENER CLIENTES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (
                nombre_cliente,
                correo_cliente,
                cliente_activo,
                fecha_creacion,
                tienda_preferida,
                direccion_cliente,
                codigo_postal_cliente,
                ciudad_cliente,
                pais_cliente) FROM tempdata WHERE tempdata.correo_cliente <> '-';""")
        customers_data = self.cursor.fetchall()

        for data in customers_data:
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # CLIENTES
            name = row[0].split(' ')
            active = 'TRUE' if row[2] == 'Si' else 'FALSE'
            c_date = row[3].split('/')
            date = f'{c_date[2]}-{c_date[1]}-{c_date[0]}'

            # QUERY CLIENTES
            self.cursor.execute(
                f"""INSERT INTO Customers (last_name, favorite, c_name, email, active, c_date)
                    VALUES ('{name[1]}', '{row[4]}', '{name[0][1:]}', '{row[1]}', {active}, '{date}');""")

        # CREAR PAISES
        self.cursor.execute("""
        CREATE TABLE Countries (
            country_id VARCHAR(250) PRIMARY KEY
        );""")

        # OBTENER PAISES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT pais_cliente FROM tempdata WHERE tempdata.pais_cliente <> '-'
               UNION
               SELECT DISTINCT pais_empleado FROM tempdata WHERE tempdata.pais_empleado <> '-'
               UNION
               SELECT DISTINCT pais_tienda FROM tempdata WHERE tempdata.pais_tienda <> '-';""")
        countries_data = self.cursor.fetchall()

        # QUERY PAISES
        for data in countries_data:
            # PAISES
            current = list(reader(data, delimiter=",", quotechar='"'))[0]
            country = ','.join(
                list(map(lambda value: value.replace('"', ""), current)))

            # QUERY CIUDADES
            self.cursor.execute(
                f"""INSERT INTO Countries VALUES ('{country}');""")

        # CREAR CIUDADES
        self.cursor.execute("""
        CREATE TABLE Cities (
            city_id SERIAL PRIMARY KEY,
            city_name VARCHAR(250),
            country_fk VARCHAR(250),
            CONSTRAINT country_fk FOREIGN KEY(country_fk) REFERENCES Countries(country_id) ON DELETE SET NULL
        );""")

        # OBTENER CIUDADES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (ciudad_cliente, pais_cliente) FROM tempdata WHERE tempdata.pais_cliente <> '-' AND tempdata.ciudad_cliente <> '-'
               UNION
               SELECT DISTINCT (ciudad_empleado, pais_empleado) FROM tempdata WHERE tempdata.pais_empleado <> '-' AND tempdata.ciudad_empleado <> '-'
               UNION
               SELECT DISTINCT (ciudad_tienda, pais_tienda) FROM tempdata WHERE tempdata.pais_tienda <> '-' AND tempdata.ciudad_tienda <> '-';""")
        cities_data = self.cursor.fetchall()

        # QUERY CIUDADES
        for data in cities_data:
            # CIUDADES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY CIUDADES
            self.cursor.execute(
                f"""INSERT INTO Cities (city_name, country_fk)
                    VALUES ('{row[0][1:]}', '{row[1][0:-1]}');""")

        # CREAR DIRECCIONES DE CIUDADES
        self.cursor.execute("""
        CREATE TABLE CityAddress (
            address_id SERIAL PRIMARY KEY,
            postal_code VARCHAR(250),
            district VARCHAR(250),
            address VARCHAR(250),
            city_fk INT,
            CONSTRAINT city_fk FOREIGN KEY(city_fk) REFERENCES Cities(city_id) ON DELETE SET NULL
        );""")

        # OBTENER DIRECCIONES CIUDADES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (direccion_cliente, codigo_postal_cliente, ciudad_cliente, pais_cliente) FROM tempdata WHERE tempdata.direccion_cliente <> '-'
               UNION
               SELECT DISTINCT (direccion_empleado, codigo_postal_empleado, ciudad_empleado, pais_empleado) FROM tempdata WHERE tempdata.direccion_empleado <> '-'
               UNION
               SELECT DISTINCT (direccion_tienda, codigo_postal_tienda, ciudad_tienda, pais_tienda) FROM tempdata WHERE tempdata.direccion_tienda <> '-';""")
        address_data = self.cursor.fetchall()

        # QUERY DIRECCIONES
        for data in address_data:
            # DIRECCIONES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            district = row[0][1:row[0].find(" ")]
            address = row[0][2+len(district):]

            # QUERY DIRECCIONES
            self.cursor.execute(
                f"""INSERT INTO CityAddress (postal_code, district, address, city_fk)
                    VALUES ({'NULL' if row[1] == '-' else "'" + row[1] + "'"}, '{district}', '{address}', (SELECT city_id from cities WHERE cities.city_name = '{row[2]}' AND cities.country_fk = '{row[3][0:-1]}'));""")

        # CREAR DIRECCIONES DE CLIENTES
        self.cursor.execute("""
        CREATE TABLE CustomerAddress (
            customer_address_id SERIAL PRIMARY KEY,
            customer_fk INT,
            address_fk INT,
            CONSTRAINT customer_fk FOREIGN KEY(customer_fk) REFERENCES Customers(customer_id) ON DELETE SET NULL,
            CONSTRAINT address_fk FOREIGN KEY(address_fk) REFERENCES CityAddress(address_id) ON DELETE SET NULL
        );""")

        # OBTENER DIRECCIONES CLIENTES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (direccion_cliente, nombre_cliente) FROM tempdata WHERE tempdata.direccion_cliente <> '-' AND tempdata.nombre_cliente <> '-';""")
        address_customer = self.cursor.fetchall()

        # QUERY DIRECCIONES
        for data in address_customer:
            # DIRECCIONES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            name = row[1][0:-1].split(' ')
            district = row[0][1:row[0].find(" ")]
            address = row[0][2+len(district):]

            # QUERY DIRECCIONES
            self.cursor.execute(
                f"""INSERT INTO CustomerAddress (customer_fk, address_fk)
                    VALUES ((SELECT customer_id FROM customers WHERE customers.c_name = '{name[0]}' AND customers.last_name = '{name[1]}'), (SELECT address_id FROM cityaddress WHERE cityaddress.address = '{address}' AND cityaddress.district = '{district}'));""")

        # CREAR TIENDAS
        self.cursor.execute("""
        CREATE TABLE Stores (
            store_id SERIAL PRIMARY KEY,
            c_name VARCHAR(250),
            address VARCHAR(250),
            district VARCHAR(250)
        );""")

        # OBTENER TIENDAS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (nombre_tienda, direccion_tienda) FROM tempdata WHERE tempdata.nombre_tienda <> '-' AND tempdata.direccion_tienda <> '-';""")
        stores_data = self.cursor.fetchall()

        # QUERY DIRECCIONES
        for data in stores_data:
            # DIRECCIONES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            name = row[0][1:]
            district = row[1][0:row[1].find(" ")]
            address = row[1][1+len(district):-1]

            # QUERY DIRECCIONES
            self.cursor.execute(
                f"""INSERT INTO Stores (c_name, address, district)
                    VALUES ('{name}', '{address}', '{district}');""")

        # CREAR EMPLEADOS
        self.cursor.execute("""
        CREATE TABLE Employees (
            employee_id SERIAL PRIMARY KEY,
            c_name VARCHAR(250),
            last_name VARCHAR(250),
            email VARCHAR(250),
            active BOOLEAN,
            user_name VARCHAR(250),
            c_password VARCHAR(250),
            store_fk INT,
            CONSTRAINT store_id FOREIGN KEY(store_fk) REFERENCES Stores(store_id) ON DELETE SET NULL
        );""")

        # CREAR DIRECCIONES DE EMPLEADOS EMPLEADOS
        self.cursor.execute("""
        CREATE TABLE EmployeeAddress (
            employee_address_id SERIAL PRIMARY KEY,
            employee_fk INT,
            address_fk INT,
            CONSTRAINT employee_fk FOREIGN KEY(employee_fk) REFERENCES Employees(employee_id) ON DELETE SET NULL,
            CONSTRAINT address_fk FOREIGN KEY(address_fk) REFERENCES CityAddress(address_id) ON DELETE SET NULL
        );""")

        # OBTENER EMPLEADOS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (
                nombre_empleado,
                correo_empleado,
                empleado_activo,
                tienda_empleado,
                usuario_empleado,
                contrasena_empleado,
                direccion_empleado) FROM tempdata WHERE tempdata.nombre_empleado <> '-' AND tempdata.correo_empleado <> '-'""")
        employees_data = self.cursor.fetchall()

        # QUERY EMPLEADOS
        employee_id = 0
        for data in employees_data:
            # EMPLEADOS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            name = row[0].split(' ')
            district = row[6][0:row[6].find(" ")]
            address = row[6][1+len(district):-1]

            # QUERY EMPLEADOS
            employee_id += 1
            self.cursor.execute(
                f"""INSERT INTO Employees (c_name, last_name, email, active, user_name, c_password, store_fk)
                    VALUES ('{name[0][1:]}', '{name[1]}', '{row[1]}', {'TRUE' if row[2] == 'Si' else 'FALSE'}, '{row[4]}', '{row[5]}', (SELECT store_id FROM stores WHERE stores.c_name = '{row[3]}'));
                    INSERT INTO EmployeeAddress (employee_fk, address_fk) VALUES ('{employee_id}', (SELECT address_id FROM cityaddress WHERE cityaddress.address = '{address}'));
                    """)

        # CREAR JEFES
        self.cursor.execute("""
        CREATE TABLE Bosses (
            boss_id SERIAL PRIMARY KEY,
            store_fk INT,
            employee_fk INT,
            CONSTRAINT store_fk FOREIGN KEY(store_fk) REFERENCES Stores(store_id) ON DELETE SET NULL,
            CONSTRAINT employee_fk FOREIGN KEY(employee_fk) REFERENCES Employees(employee_id) ON DELETE SET NULL
        );""")

        # OBTENER JEFES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (encargado_tienda, nombre_tienda) FROM tempdata WHERE tempdata.encargado_tienda <> '-'""")
        bosses_data = self.cursor.fetchall()

        # QUERY JEFES
        for data in bosses_data:
            # JEFES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            name = row[0][1:].split(' ')

            # QUERY JEFES
            self.cursor.execute(
                f"""INSERT INTO Bosses (store_fk, employee_fk)
                    VALUES ((SELECT store_id FROM stores WHERE stores.c_name = '{row[1][0:-1]}'), (SELECT employee_id FROM employees WHERE employees.c_name = '{name[0]}' AND employees.last_name = '{name[1]}'));""")

        # CREAR PELICULAS
        self.cursor.execute("""
        CREATE TABLE Movies (
            movie_id SERIAL PRIMARY KEY,
            description VARCHAR(250),
            m_type VARCHAR(250),
            title VARCHAR(250),
            m_duration INT,
            price DECIMAL,
            year INT,
            days INT,
            fee DECIMAL
          );""")

        # OBTENER PELICULAS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (
                nombre_pelicula,
                descripcion_pelicula,
                ano_lanzamiento,
                dias_renta,
                costo_renta,
                duracion,
                costo_por_dano,
                clasificacion) FROM TEMPDATA WHERE tempdata.nombre_pelicula <> '-' AND tempdata.tienda_pelicula <> '-';""")
        movies_data = self.cursor.fetchall()

        # QUERY PELICULAS
        for data in movies_data:
            # PELICULAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY PELICULAS
            self.cursor.execute(
                f"""INSERT INTO Movies (description, m_type, title, m_duration, price, year, days, fee)
                    VALUES ('{row[1]}', '{row[7][0:-1]}', '{row[0][1:]}', '{row[5]}', '{row[4]}', '{row[2]}', '{row[3]}', '{row[6]}');""")

        # CREAR INVENTARIO
        self.cursor.execute("""
        CREATE TABLE Stocks (
            stock_id SERIAL PRIMARY KEY,
            movie_fk INT,
            store_fk INT,
            CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE SET NULL,
            CONSTRAINT store_fk FOREIGN KEY(store_fk) REFERENCES Stores(store_id) ON DELETE SET NULL
          );""")

        # OBTENER INVENTARIO DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (nombre_pelicula, nombre_tienda) FROM TEMPDATA WHERE tempdata.nombre_pelicula <> '-' AND tempdata.nombre_tienda <> '-';""")
        stocks_data = self.cursor.fetchall()

        # QUERY INVENTARIO
        for data in stocks_data:
            # INVENTARIO
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY INVENTARIO
            self.cursor.execute(
                f"""INSERT INTO Stocks (movie_fk, store_fk)
                    VALUES (
                    (SELECT movie_id FROM movies WHERE movies.title = '{row[0][1:]}'), 
                    (SELECT store_id FROM stores WHERE stores.c_name = '{row[1][0:-1]}'));""")

        # CREAR CATEGORIAS
        self.cursor.execute("""
        CREATE TABLE Categories (
            category_id VARCHAR(250) PRIMARY KEY
        );""")

        # OBTENER CATEGORIAS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (categoria_pelicula) FROM tempdata WHERE tempdata.categoria_pelicula <> '-' AND tempdata.nombre_pelicula <> '-';""")
        categories_data = self.cursor.fetchall()

        # QUERY CATEGORIAS
        for data in categories_data:
            # CATEGORIAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY CATEGORIAS
            self.cursor.execute(
                f"""INSERT INTO Categories (category_id)
                    VALUES ('{row[0]}');""")

        # CREAR CATEGORIA-PELICULA
        self.cursor.execute("""
        CREATE TABLE MovieCategories (
            movie_category_id SERIAL PRIMARY KEY,
            movie_fk INT,
            category_fk VARCHAR(250),
            CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE SET NULL,
            CONSTRAINT category_fk FOREIGN KEY(category_fk) REFERENCES Categories(category_id) ON DELETE SET NULL
        );""")

        # OBTENER CATEGORIAS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (nombre_pelicula, categoria_pelicula, ano_lanzamiento, duracion, clasificacion) FROM tempdata WHERE tempdata.categoria_pelicula <> '-' AND tempdata.nombre_pelicula <> '-';""")
        movie_categories_data = self.cursor.fetchall()

        # QUERY CATEGORIAS PELICULAS
        for data in movie_categories_data:
            # CATEGORIAS PELICULAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY CATEGORIAS PELICULAS
            self.cursor.execute(
                f"""INSERT INTO MovieCategories (movie_fk, category_fk)
                    VALUES ((SELECT movie_id FROM movies WHERE movies.title = '{row[0][1:]}' AND movies.year = '{row[2]}' AND movies.m_duration = '{row[3]}' AND movies.m_type = '{row[4][0:-1]}'), '{row[1]}');""")

        # CREAR ACTORES
        self.cursor.execute("""
        CREATE TABLE Actors (
            actor_id SERIAL PRIMARY KEY,
            c_name VARCHAR(250),
            last_name VARCHAR(250)
        );""")

        # OBTENER ACTORES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (actor_pelicula) FROM tempdata WHERE tempdata.actor_pelicula <> '-' AND tempdata.nombre_pelicula <> '-';""")
        actors_data = self.cursor.fetchall()

        # QUERY ACTORES
        for data in actors_data:
            # ACTORES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            name = row[0].split(' ')

            # QUERY ACTORES
            self.cursor.execute(
                f"""INSERT INTO Actors (c_name, last_name)
                    VALUES ('{name[0]}', '{name[1]}');""")

        # CREAR ACTORES-PELICULA
        self.cursor.execute("""
        CREATE TABLE MovieActors (
            movie_actor_id SERIAL PRIMARY KEY,
            movie_fk INT,
            actor_fk INT,
            CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE SET NULL,
            CONSTRAINT actor_fk FOREIGN KEY(actor_fk) REFERENCES Actors(actor_id) ON DELETE SET NULL
        );""")

        # OBTENER ACTORES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (nombre_pelicula, actor_pelicula, ano_lanzamiento, duracion, clasificacion) FROM tempdata WHERE tempdata.actor_pelicula <> '-' AND tempdata.nombre_pelicula <> '-';""")
        movie_actors_data = self.cursor.fetchall()

        # QUERY ACTORES PELICULAS
        for data in movie_actors_data:
            # ACTORES PELICULAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            name = row[1].split(' ')

            # QUERY ACTORES PELICULAS
            self.cursor.execute(
                f"""INSERT INTO MovieActors (movie_fk, actor_fk)
                    VALUES ((SELECT movie_id FROM movies WHERE movies.title = '{row[0][1:]}' AND movies.year = '{row[2]}' AND movies.m_duration = '{row[3]}' AND movies.m_type = '{row[4][0:-1]}'), (SELECT actor_id FROM actors WHERE actors.c_name = '{name[0]}' AND actors.last_name = '{name[1]}'));""")

        # CREAR ACTORES
        self.cursor.execute("""
        CREATE TABLE Translates (
            translate_id VARCHAR(250) PRIMARY KEY
        );""")

        # OBTENER ACTORES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (lenguaje_pelicula) FROM tempdata WHERE tempdata.lenguaje_pelicula <> '-';""")
        langs_data = self.cursor.fetchall()

        # QUERY ACTORES
        for data in langs_data:
            # ACTORES
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY ACTORES
            self.cursor.execute(
                f"""INSERT INTO Translates (translate_id)
                    VALUES ('{row[0]}');""")

        # CREAR ACTORES-PELICULA
        self.cursor.execute("""
        CREATE TABLE MovieTranslates (
            movie_lang_id SERIAL PRIMARY KEY,
            movie_fk INT,
            translate_fk VARCHAR(250),
            CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE SET NULL,
            CONSTRAINT translate_fk FOREIGN KEY(translate_fk) REFERENCES Translates(translate_id) ON DELETE SET NULL
        );""")

        # OBTENER ACTORES DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (nombre_pelicula, lenguaje_pelicula, ano_lanzamiento, duracion, clasificacion) FROM tempdata WHERE tempdata.lenguaje_pelicula <> '-' AND tempdata.nombre_pelicula <> '-';""")
        movie_langs_data = self.cursor.fetchall()

        # QUERY ACTORES PELICULAS
        for data in movie_langs_data:
            # ACTORES PELICULAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))

            # QUERY ACTORES PELICULAS
            self.cursor.execute(
                f"""INSERT INTO MovieTranslates (movie_fk, translate_fk)
                    VALUES ((SELECT movie_id FROM movies WHERE movies.title = '{row[0][1:]}' AND movies.year = '{row[2]}' AND movies.m_duration = '{row[3]}' AND movies.m_type = '{row[4][0:-1]}'), '{row[1]}');""")

        # CREAR RENTAS
        self.cursor.execute("""
        CREATE TABLE Rents (
            rent_id SERIAL PRIMARY KEY,
            amount DECIMAL,
            pay_date TIMESTAMP,
            date_in TIMESTAMP,
            date_out TIMESTAMP);""")

        # OBTENER RENTAS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (fecha_pago, fecha_renta, fecha_retorno, monto_a_pagar) FROM tempdata WHERE tempdata.fecha_pago <> '-' AND tempdata.fecha_renta <> '-'""")
        rents_data = self.cursor.fetchall()

        # QUERY RENTAS
        for data in rents_data:
            # RENTAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            pay_date = self.date_to_timestamp(row[0][1:])
            date_in = self.date_to_timestamp(row[1])
            date_out = f"'{self.date_to_timestamp(row[2])}'" if row[2] != '-' else 'NULL'

            # QUERY RENTAS
            self.cursor.execute(
                f"""INSERT INTO Rents (amount, pay_date, date_in, date_out)
                    VALUES ('{row[3][0:-1]}', '{pay_date}', '{date_in}', {date_out});""")

        # CREAR FACTURAS
        self.cursor.execute("""
        CREATE TABLE Bills (
            bill_id SERIAL PRIMARY KEY,
            employee_fk INT,
            customer_fk INT,
            movie_fk INT,
            rent_fk INT,
            CONSTRAINT employee_fk FOREIGN KEY(employee_fk) REFERENCES Employees(employee_id) ON DELETE SET NULL,
            CONSTRAINT customer_fk FOREIGN KEY(customer_fk) REFERENCES Customers(customer_id) ON DELETE SET NULL,
            CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE SET NULL,
            CONSTRAINT rent_fk FOREIGN KEY(rent_fk) REFERENCES Rents(rent_id) ON DELETE SET NULL
        );""")

        # OBTENER FACTURAS DE TEMPORAL
        self.cursor.execute(
            """SELECT DISTINCT (nombre_empleado, nombre_cliente, nombre_pelicula, fecha_renta, fecha_pago, fecha_retorno, monto_a_pagar) FROM tempdata WHERE tempdata.fecha_renta <> '-' AND tempdata.nombre_empleado <> '-' AND tempdata.nombre_cliente <> '-' AND tempdata.nombre_pelicula <> '-';""")
        bills_data = self.cursor.fetchall()

        # QUERY FACTURAS
        for data in bills_data:
            # FACTURAS
            current = list(reader(data, delimiter=","))[0]
            row = list(map(lambda value: value.replace('"', ""), current))
            employee_name = row[0][1:].split(' ')
            customer_name = row[1].split(' ')
            date_in = self.date_to_timestamp(row[3])
            pay_date = self.date_to_timestamp(row[4])
            date_out = f"'{self.date_to_timestamp(row[5])}'" if row[5] != '-' else 'NULL'

            # QUERY FACTURAS
            self.cursor.execute(
                f"""INSERT INTO Bills (employee_fk, customer_fk, movie_fk, rent_fk)
                    VALUES (
                    (SELECT employee_id FROM employees WHERE employees.c_name = '{employee_name[0]}' AND employees.last_name = '{employee_name[1]}'),
                    (SELECT customer_id FROM customers WHERE customers.c_name = '{customer_name[0]}' AND customers.last_name = '{customer_name[1]}'),
                    (SELECT movie_id FROM movies WHERE movies.title = '{row[2]}'),
                    (SELECT rent_id FROM rents WHERE rents.date_in = '{date_in}' AND rents.amount = '{row[6][0:-1]}' AND rents.pay_date = '{pay_date}' AND rents.date_out = {date_out}));""")

        self.connect.commit()
        return "Modelo cargado correctamente"

    # ELIMINAR TEMPORAl
    def delete_temporal(self):
        self.exectue_psql('deleteTemp')
        return "Tabla temporal borrada correctamente"

    # ELIMINAR MODELO
    def delete_model(self):
        self.exectue_psql('deleteModel')
        return "Modelos borrados correctamente"

    # SERIALIZAR LISTAS
    def serialize_list(self, rows):
        tmp = list(map(lambda row: list(
            map(lambda col: str(col), row)), rows))
        out = jsonify(tmp)
        return out

    # EJECUTAR CONSULTA N
    def run_query_n(self, n):
        self.exectue_psql(f'frequent/query_{n}', False)
        rows = self.cursor.fetchall()
        self.connect.commit()
        return f"Total de peliculas en inventario con SUGAR WONKA = {rows[0][0]}" if n == 1 else self.serialize_list(
            rows)
