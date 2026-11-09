CREATE OR REPLACE TABLE accounts (
    account_id INTEGER, account_name VARCHAR, owner_id INTEGER, region VARCHAR, created_at DATE
);
INSERT INTO accounts VALUES
 (1,'Acme Corp',10,'west','2024-01-15'),
 (2,'Globex',11,'east','2024-02-20'),
 (3,'Initech',NULL,'central','2024-03-10'),
 (4,'Umbrella',12,'west','2023-10-01'),
 (4,'Umbrella',12,'west','2023-10-01'),
 (5,'Stark Industries',13,'east','2024-03-25');

CREATE OR REPLACE TABLE plan_accounts (plan_id INTEGER, account_id INTEGER);
INSERT INTO plan_accounts VALUES (1,1),(2,2),(3,5),(4,999);
