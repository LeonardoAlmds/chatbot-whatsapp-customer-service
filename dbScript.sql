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

CREATE TABLE product_imgs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    img_url VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
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

INSERT INTO product_imgs (product_id, img_url)
VALUES (1, 'https://www.apple.com/newsroom/images/product/iphone/standard/Apple_announce-iphone12pro_10132020_big.jpg.large.jpg'),
    (2, 'https://a-static.mlcdn.com.br/800x560/usado-samsung-galaxy-s21-fe-6gb-5g-128gb-preto-bom-trocafone/trocafone/58905/bebaa41a81fdbcc7abf33f0e3ac7419b.jpeg'),
    (3, 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp-spacegray-select-202011?wid=892&hei=820&&qlt=80&.v=1603406905000'),
    (4, 'https://compass-ssl.microsoft.com/assets/0d/0d/0d0d1b9b-0b1e-4b1e-8b1e-3b1e8b1e8b1e.jpg?n=Surface_Pro_7_1.jpg'),
    (5, 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-12-select-wifi-spacegray-202104_FMT_WHH?wid=940&hei=1112&fmt=jpeg&qlt=80&.v=1617126627000');


SELECT * FROM products;
SELECT * FROM categories;
SELECT * FROM brands;
SELECT * FROM product_imgs;

SELECT p.name, p.price, pi.img_url
        FROM products p
        INNER JOIN product_imgs pi ON p.id = pi.product_id
        WHERE p.name = 'Iphone 12';