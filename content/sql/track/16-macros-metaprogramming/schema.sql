CREATE OR REPLACE TABLE source_a (id INTEGER, name VARCHAR, amount DECIMAL(10,2), created_at TIMESTAMP);
INSERT INTO source_a VALUES (1,'Acme',100.00,'2024-01-01 00:00:00'),(2,'Globex',200.00,'2024-01-02 00:00:00');

CREATE OR REPLACE TABLE source_b (id INTEGER, name VARCHAR, amount_usd VARCHAR, created_ts TIMESTAMP);
INSERT INTO source_b VALUES (2,'Globex Updated','250.00','2024-02-01 00:00:00'),(3,'Initech','300.00','2024-01-03 00:00:00');

CREATE OR REPLACE TABLE columns_metadata (column_name VARCHAR, data_type VARCHAR);
INSERT INTO columns_metadata VALUES
 ('id','INTEGER'),('name','VARCHAR'),('amount','DECIMAL'),('created_at','TIMESTAMP_TZ'),('updated_at','TIMESTAMP_TZ'),('region','VARCHAR');
