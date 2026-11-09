CREATE OR REPLACE TABLE source_accounts (
    account_id INTEGER, account_name VARCHAR, segment VARCHAR
);
INSERT INTO source_accounts VALUES
 (1,'Acme Corp','enterprise'),(2,'Globex','mid_market'),(3,'Initech','smb'),(4,'Umbrella','enterprise');

CREATE OR REPLACE TABLE source_subscriptions (
    sub_id INTEGER, account_id INTEGER, plan_code VARCHAR, start_date DATE, end_date DATE, mrr DECIMAL(10,2), is_trial BOOLEAN
);
INSERT INTO source_subscriptions VALUES
 (1,1,'enterprise_annual','2023-01-01',NULL,2000.00,false),
 (2,2,'growth_monthly','2023-02-01',NULL,500.00,false),
 (3,3,'starter_monthly','2023-03-01','2023-06-01',49.00,true),
 (4,1,'addon_support','2023-04-01',NULL,300.00,false),
 (5,99,'growth_monthly','2023-05-01',NULL,500.00,false),
 (6,4,'enterprise_annual','2023-06-01',NULL,2200.00,false);

CREATE OR REPLACE TABLE legacy_subscriptions (account_id INTEGER, plan_code VARCHAR);
INSERT INTO legacy_subscriptions VALUES (2,'legacy_basic'), (3,'legacy_basic');
