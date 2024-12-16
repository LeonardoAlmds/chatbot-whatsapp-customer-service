CREATE DATABASE Restaurant;
USE Restaurant;

CREATE TABLE plates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plate_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (plate_id) REFERENCES plates(id)
);

CREATE TABLE tables (
    id INT PRIMARY KEY AUTO_INCREMENT,
    number INT NOT NULL
);

CREATE TABLE orders_tables (
    order_id INT NOT NULL,
    table_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (table_id) REFERENCES tables(id)
);

SELECT * FROM plates;
SELECT * FROM orders;
SELECT * FROM tables;
SELECT * FROM orders_tables;

INSERT INTO plates (name, price) VALUES ('Pizza', 10.00);
INSERT INTO plates (name, price) VALUES ('Pasta', 8.00);
INSERT INTO plates (name, price) VALUES ('Salad', 5.00);
INSERT INTO plates (name, price) VALUES ('Bread', 2.00);
INSERT INTO plates (name, price) VALUES ('Water', 1.00);
INSERT INTO plates (name, price) VALUES ('Soda', 2.00);

INSERT INTO tables (number) VALUES (1);
INSERT INTO tables (number) VALUES (2);
INSERT INTO tables (number) VALUES (3);
INSERT INTO tables (number) VALUES (4);

INSERT INTO orders (plate_id, quantity) VALUES (1, 2);
INSERT INTO orders (plate_id, quantity) VALUES (2, 1);
INSERT INTO orders (plate_id, quantity) VALUES (3, 3);
INSERT INTO orders (plate_id, quantity) VALUES (4, 1);
INSERT INTO orders (plate_id, quantity) VALUES (5, 4);

INSERT INTO orders_tables (order_id, table_id) VALUES (1, 1);
INSERT INTO orders_tables (order_id, table_id) VALUES (2, 2);
INSERT INTO orders_tables (order_id, table_id) VALUES (3, 3);
INSERT INTO orders_tables (order_id, table_id) VALUES (4, 4);
INSERT INTO orders_tables (order_id, table_id) VALUES (5, 1);

