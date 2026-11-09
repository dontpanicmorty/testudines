CREATE OR REPLACE TABLE accounts_multi (account_key INTEGER, accountid_a VARCHAR, accountid_b VARCHAR, account_name VARCHAR);
INSERT INTO accounts_multi VALUES
 (1,'A100',NULL,'Acme Corp'),
 (2,NULL,'B200','Globex'),
 (3,'A300','B300','Initech');

CREATE OR REPLACE TABLE territory_plan (plan_id INTEGER, accountid_a VARCHAR, accountid_b VARCHAR, territory VARCHAR, priority INTEGER);
INSERT INTO territory_plan VALUES
 (10,'A100',NULL,'west',1),
 (14,'A100',NULL,'west_backup',5),
 (11,NULL,'B200','east',2),
 (12,'A300',NULL,'central',1),
 (13,NULL,'B300','central2',2);

CREATE OR REPLACE TABLE web_contracts (contract_id INTEGER, accountid_a VARCHAR, contract_value DECIMAL(10,2));
INSERT INTO web_contracts VALUES (1,'A100',5000.00),(2,'A300',3000.00);
