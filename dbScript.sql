CREATE DATABASE whatsappPy;
USE whatsappPy;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    last_message VARCHAR(50)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO products (name, price, category, brand) VALUES ('Iphone 12', 1200, 'smartphone', 'Apple');
INSERT INTO products (name, price, category, brand) VALUES ('Galaxy S21', 1000, 'smartphone', 'Samsung');
INSERT INTO products (name, price, category, brand) VALUES ('Macbook Pro', 2000, 'laptop', 'Apple');
INSERT INTO products (name, price, category, brand) VALUES ('Surface Pro', 1500, 'laptop', 'Microsoft');
INSERT INTO products (name, price, category, brand) VALUES ('Ipad Pro', 800, 'tablet', 'Apple');
INSERT INTO products (name, price, category, brand) VALUES ('Galaxy Tab', 600, 'tablet', 'Samsung');
INSERT INTO products (name, price, category, brand) VALUES ('Airpods Pro', 250, 'earbuds', 'Apple');

INSERT INTO categories (name) VALUES ('smartphone');
INSERT INTO categories (name) VALUES ('laptop');
INSERT INTO categories (name) VALUES ('tablet');
INSERT INTO categories (name) VALUES ('earbuds');

INSERT INTO brands (name) VALUES ('Apple');
INSERT INTO brands (name) VALUES ('Samsung');
INSERT INTO brands (name) VALUES ('Microsoft');

SELECT * FROM products;

DROP TABLE users;