DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS product_imgs;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL,
    brand_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

INSERT INTO categories (name) VALUES ('smartphone'), ('laptop'), ('tablet'), ('earbuds');
INSERT INTO brands (name) VALUES ('Apple'), ('Samsung'), ('Microsoft');

INSERT INTO products (name, price, category_id, brand_id)
VALUES ('Iphone 12', 1200, 1, 1),
    ('Galaxy S21', 1000, 1, 2),
    ('Macbook Pro', 2000, 2, 1),
    ('Surface Pro', 1500, 2, 3),
    ('Ipad Pro', 800, 3, 1),
    ('Galaxy Tab', 600, 3, 2),
    ('Airpods Pro', 250, 4, 1);

SELECT * FROM products;
SELECT * FROM categories;
SELECT * FROM brands;