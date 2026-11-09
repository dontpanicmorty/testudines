CREATE OR REPLACE TABLE customers (
    customer_id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    region VARCHAR,
    signup_date DATE,
    is_active BOOLEAN
);
INSERT INTO customers VALUES
 (1,'Ava','Chen','west','2023-01-15',true),
 (2,'Noah','Diaz','east','2023-03-02',true),
 (3,'Mia','Patel','west','2022-11-20',false),
 (4,'Liam','Nguyen','central','2023-06-10',true),
 (5,'Zoe','Okafor','east','2021-09-05',false),
 (6,'Ethan','Brooks','west','2024-02-18',true);

CREATE OR REPLACE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    amount DECIMAL(10,2),
    status VARCHAR
);
INSERT INTO orders VALUES
 (100,1,'2023-02-01',49.99,'completed'),
 (101,1,'2023-03-05',19.99,'completed'),
 (102,2,'2023-04-10',99.50,'completed'),
 (103,3,'2022-12-01',15.00,'refunded'),
 (104,4,'2023-07-01',150.00,'completed'),
 (105,6,'2024-03-01',75.25,'pending'),
 (106,2,'2023-05-15',30.00,'completed');
