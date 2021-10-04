-- SCHEMA: public;
GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

SET client_encoding = WIN1252;

/* CLIENTES */
DROP TABLE IF EXISTS Customers CASCADE;

CREATE TABLE Customers (
  customer_id SERIAL PRIMARY KEY,
  last_name VARCHAR(250),
  favorite VARCHAR(250),
  c_name VARCHAR(250),
  email VARCHAR(250),
  active BOOLEAN,
  c_date DATE
);

DROP TABLE IF EXISTS Countries CASCADE;

CREATE TABLE Countries (country_id VARCHAR(250) PRIMARY KEY);

DROP TABLE IF EXISTS Cities CASCADE;

CREATE TABLE Cities (
  city_id SERIAL PRIMARY KEY,
  city_name VARCHAR(250),
  country_fk VARCHAR(250),
  CONSTRAINT country_fk FOREIGN KEY(country_fk) REFERENCES Countries(country_id) ON DELETE
  SET NULL
);

DROP TABLE IF EXISTS CityAddress CASCADE;

CREATE TABLE CityAddress (
  address_id SERIAL PRIMARY KEY,
  postal_code VARCHAR(250),
  district VARCHAR(250),
  address VARCHAR(250),
  city_fk INT,
  CONSTRAINT city_fk FOREIGN KEY(city_fk) REFERENCES Cities(city_id) ON DELETE
  SET NULL
);

DROP TABLE IF EXISTS CustomerAddress CASCADE;

CREATE TABLE CustomerAddress (
  customer_address_id SERIAL PRIMARY KEY,
  customer_fk INT,
  address_fk INT,
  CONSTRAINT customer_fk FOREIGN KEY(customer_fk) REFERENCES Customers(customer_id) ON DELETE
  SET NULL,
    CONSTRAINT address_fk FOREIGN KEY(address_fk) REFERENCES CityAddress(address_id) ON DELETE
  SET NULL
);

/* NEGOCIO */
DROP TABLE IF EXISTS Stores CASCADE;

CREATE TABLE Stores (
  store_id SERIAL PRIMARY KEY,
  c_name VARCHAR(250),
  address VARCHAR(250),
  district VARCHAR(250)
);

DROP TABLE IF EXISTS Employees CASCADE;

CREATE TABLE Employees (
  employee_id SERIAL PRIMARY KEY,
  c_name VARCHAR(250),
  last_name VARCHAR(250),
  email VARCHAR(250),
  active BOOLEAN,
  user_name VARCHAR(250),
  c_password VARCHAR(250),
  store_fk INT,
  CONSTRAINT store_id FOREIGN KEY(store_fk) REFERENCES Stores(store_id) ON DELETE
  SET NULL
);

DROP TABLE IF EXISTS EmployeeAddress CASCADE;

CREATE TABLE EmployeeAddress (
  employee_address_id SERIAL PRIMARY KEY,
  employee_fk INT,
  address_fk INT,
  CONSTRAINT employee_fk FOREIGN KEY(employee_fk) REFERENCES Employees(employee_id) ON DELETE
  SET NULL,
    CONSTRAINT address_fk FOREIGN KEY(address_fk) REFERENCES CityAddress(address_id) ON DELETE
  SET NULL
);

DROP TABLE IF EXISTS Bosses CASCADE;

CREATE TABLE Bosses (
  boss_id SERIAL PRIMARY KEY,
  store_fk INT,
  employee_fk INT,
  CONSTRAINT store_fk FOREIGN KEY(store_fk) REFERENCES Stores(store_id) ON DELETE
  SET NULL,
    CONSTRAINT employee_fk FOREIGN KEY(employee_fk) REFERENCES Employees(employee_id) ON DELETE
  SET NULL
);

/* PELICULAS */
DROP TABLE IF EXISTS Stocks CASCADE;

CREATE TABLE Stocks (
  stock_id SERIAL PRIMARY KEY,
  store_fk INT,
  CONSTRAINT store_fk FOREIGN KEY(store_fk) REFERENCES Stores(store_id) ON DELETE
);

DROP TABLE IF EXISTS Movies CASCADE;

CREATE TABLE Movies (
  movie_id SERIAL PRIMARY KEY,
  description VARCHAR(250),
  m_type VARCHAR(250),
  title VARCHAR(250),
  m_duration INT,
  price DECIMAL,
  year INT,
  days INT,
  fee DECIMAL,
  stock_fk INT,
  CONSTRAINT stock_fk FOREIGN KEY(stock_fk) REFERENCES Stocks(store_id) ON DELETE
);

DROP TABLE IF EXISTS Categories CASCADE;

CREATE TABLE Categories (category_id VARCHAR(250) PRIMARY KEY);

DROP TABLE IF EXISTS MovieCategories CASCADE;

CREATE TABLE MovieCategories (
  movie_category_id SERIAL PRIMARY KEY,
  movie_fk INT,
  category_fk VARCHAR(250),
  CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE
  SET NULL,
    CONSTRAINT category_fk FOREIGN KEY(category_fk) REFERENCES Categories(category_id) ON DELETE
  SET NULL
);

DROP TABLE IF EXISTS Actors CASCADE;

CREATE TABLE Actors (
  actor_id SERIAL PRIMARY KEY,
  c_name VARCHAR(250),
  last_name VARCHAR(250)
);

DROP TABLE IF EXISTS MovieActors CASCADE;

CREATE TABLE MovieActors (
  movie_actor_id SERIAL PRIMARY KEY,
  movie_fk INT,
  actor_fk INT,
  CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE
  SET NULL,
    CONSTRAINT actor_fk FOREIGN KEY(actor_fk) REFERENCES Actors(actor_id) ON DELETE
  SET NULL
);

DROP TABLE IF EXISTS Translates CASCADE;

CREATE TABLE Translates (translate_id VARCHAR(250) PRIMARY KEY);

DROP TABLE IF EXISTS MovieTranslates CASCADE;

CREATE TABLE MovieTranslates (
  movie_lang_id SERIAL PRIMARY KEY,
  movie_fk INT,
  translate_fk VARCHAR(250),
  CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE
  SET NULL,
    CONSTRAINT translate_fk FOREIGN KEY(translate_fk) REFERENCES Translates(translate_id) ON DELETE
  SET NULL
);

/* FACTURAS */
DROP TABLE IF EXISTS Rents CASCADE;

CREATE TABLE Rents (
  rent_id SERIAL PRIMARY KEY,
  amount DECIMAL,
  pay_date TIMESTAMP,
  date_in TIMESTAMP,
  date_out TIMESTAMP
);

DROP TABLE IF EXISTS Bills CASCADE;

CREATE TABLE Bills (
  bill_id SERIAL PRIMARY KEY,
  employee_fk INT,
  customer_fk INT,
  movie_fk INT,
  rent_fk INT,
  CONSTRAINT employee_fk FOREIGN KEY(employee_fk) REFERENCES Employees(employee_id) ON DELETE
  SET NULL,
    CONSTRAINT customer_fk FOREIGN KEY(customer_fk) REFERENCES Customers(customer_id) ON DELETE
  SET NULL,
    CONSTRAINT movie_fk FOREIGN KEY(movie_fk) REFERENCES Movies(movie_id) ON DELETE
  SET NULL,
    CONSTRAINT rent_fk FOREIGN KEY(rent_fk) REFERENCES Rents(rent_id) ON DELETE
  SET NULL
);