// SQL Dojo curriculum: 20 lessons x 5 modules = 100 exercises, grouped and ordered by
// difficulty (lessons 1-6 easy, 7-12 medium, 13-20 hard; 30 easy / 30 medium / 40 hard total).
// Patterns modeled on real idioms found in this repo's models/, macros/, snapshots/, tests/
// (staging CTEs, QUALIFY dedup, incremental configs, snapshots, surrogate keys, semi-structured
// data, macro-style metaprogramming, multi-source COALESCE joins, string/date/null handling,
// advanced joins, dbt test simulation, recursive CTEs, JSON construction, and pivoting), using
// fake sample data, not this repo's real business data.

const LESSONS = [
  {
    "id": 1,
    "difficulty": "easy",
    "title": "SQL Fundamentals"
  },
  {
    "id": 2,
    "difficulty": "easy",
    "title": "Joins & Aggregation"
  },
  {
    "id": 3,
    "difficulty": "easy",
    "title": "String Functions & Formatting"
  },
  {
    "id": 4,
    "difficulty": "easy",
    "title": "NULL Handling & Boolean Logic"
  },
  {
    "id": 5,
    "difficulty": "easy",
    "title": "Basic Date Parts"
  },
  {
    "id": 6,
    "difficulty": "easy",
    "title": "Set Operations & Simple Subqueries"
  },
  {
    "id": 7,
    "difficulty": "medium",
    "title": "CTEs & the Staging Pattern"
  },
  {
    "id": 8,
    "difficulty": "medium",
    "title": "Window Functions & Dedup"
  },
  {
    "id": 9,
    "difficulty": "medium",
    "title": "Testing, Jinja Concepts & Dates"
  },
  {
    "id": 10,
    "difficulty": "medium",
    "title": "More Window Functions"
  },
  {
    "id": 11,
    "difficulty": "medium",
    "title": "Advanced Joins"
  },
  {
    "id": 12,
    "difficulty": "medium",
    "title": "dbt Testing & Static Reference Data"
  },
  {
    "id": 13,
    "difficulty": "hard",
    "title": "Incremental Models"
  },
  {
    "id": 14,
    "difficulty": "hard",
    "title": "Semi-Structured Data"
  },
  {
    "id": 15,
    "difficulty": "hard",
    "title": "Snapshots & Surrogate Keys"
  },
  {
    "id": 16,
    "difficulty": "hard",
    "title": "Macros & Metaprogramming"
  },
  {
    "id": 17,
    "difficulty": "hard",
    "title": "Advanced Multi-Source Integration"
  },
  {
    "id": 18,
    "difficulty": "hard",
    "title": "Recursive CTEs"
  },
  {
    "id": 19,
    "difficulty": "hard",
    "title": "Building Semi-Structured Data"
  },
  {
    "id": 20,
    "difficulty": "hard",
    "title": "Conditional Aggregation & Pivoting"
  }
];

// Shared CREATE TABLE + INSERT fixtures, reused across every module in a lesson
// that trades against the same sample tables (extracted to cut down on copy-paste
// across ~100 modules; see MODULES below for which module uses which schema).
const SCHEMAS = {
  customersOrders: `
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
`,
  customersOrders1: `
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

ALTER TABLE customers ADD COLUMN referral_source VARCHAR;
UPDATE customers SET referral_source = 'paid_search' WHERE customer_id IN (1,4);
UPDATE customers SET referral_source = 'partner' WHERE customer_id = 2;
`,
  customers: `CREATE OR REPLACE TABLE customers (customer_id INTEGER, first_name VARCHAR, email VARCHAR);
INSERT INTO customers VALUES
  (1, 'Ana', 'Ana.Lopez@Example.com'),
  (2, 'Ben', 'BEN.KIM@EXAMPLE.COM'),
  (3, 'Cara', 'cara.diaz@example.com'),
  (4, 'Deo', 'Deo.Singh@Example.COM');`,
  customers1: `CREATE OR REPLACE TABLE customers (customer_id INTEGER, raw_name VARCHAR);
INSERT INTO customers VALUES
  (1, '  Ana Lopez'),
  (2, 'Ben Kim   '),
  (3, '  Cara Diaz  '),
  (4, 'Deo Singh');`,
  employees: `CREATE OR REPLACE TABLE employees (employee_id INTEGER, first_name VARCHAR, last_name VARCHAR);
INSERT INTO employees VALUES
  (1, 'Ana', 'Lopez'),
  (2, 'Ben', 'Kim'),
  (3, 'Cara', 'Diaz'),
  (4, 'Deo', 'Singh');`,
  products: `CREATE OR REPLACE TABLE products (product_id INTEGER, sku VARCHAR);
INSERT INTO products VALUES
  (1, 'ELEC-1001'),
  (2, 'ELEC-1002'),
  (3, 'HOME-2001'),
  (4, 'TOYS-3001'),
  (5, 'HOME-2002');`,
  supportTickets: `CREATE OR REPLACE TABLE support_tickets (ticket_id INTEGER, description VARCHAR);
INSERT INTO support_tickets VALUES
  (1, '{{customer}} cannot log in'),
  (2, 'Billing question from {{customer}}'),
  (3, '{{customer}} requests refund'),
  (4, 'App crash reported by {{customer}}');`,
  accounts: `CREATE OR REPLACE TABLE accounts (account_id INTEGER, plan_name VARCHAR, cancelled_at DATE);
INSERT INTO accounts VALUES
  (1, 'starter', NULL),
  (2, 'pro', '2025-02-01'),
  (3, 'starter', NULL),
  (4, 'enterprise', NULL),
  (5, 'pro', '2025-05-15');`,
  campaigns: `CREATE OR REPLACE TABLE campaigns (campaign_id INTEGER, clicks INTEGER, impressions INTEGER);
INSERT INTO campaigns VALUES
  (1, 10, 100),
  (2, 0, 0),
  (3, 25, 500),
  (4, 5, 0);`,
  subscriptions: `CREATE OR REPLACE TABLE subscriptions (subscription_id INTEGER, plan_name VARCHAR, status VARCHAR, is_trial BOOLEAN);
INSERT INTO subscriptions VALUES
  (1, 'starter', 'active', false),
  (2, 'starter', 'active', true),
  (3, 'enterprise', 'active', true),
  (4, 'pro', 'cancelled', false),
  (5, 'enterprise', 'cancelled', false);`,
  events: `CREATE OR REPLACE TABLE events (event_id INTEGER, event_type VARCHAR);
INSERT INTO events VALUES
  (1, 'signup'),
  (2, 'login'),
  (3, 'upgrade'),
  (4, 'logout'),
  (5, 'renewal'),
  (6, 'cancellation');`,
  leads: `CREATE OR REPLACE TABLE leads (lead_id INTEGER, source VARCHAR, converted_at DATE, is_qualified BOOLEAN);
INSERT INTO leads VALUES
  (1, 'ads', '2025-01-05', true),
  (2, 'ads', NULL, true),
  (3, 'referral', NULL, NULL),
  (4, 'organic', '2025-02-10', false),
  (5, 'referral', '2025-03-01', false);`,
  orders: `CREATE OR REPLACE TABLE orders (order_id INTEGER, order_date DATE);
INSERT INTO orders VALUES
  (1, '2025-01-15'),
  (2, '2025-03-22'),
  (3, '2025-03-30'),
  (4, '2024-12-01');`,
  events1: `CREATE OR REPLACE TABLE events (event_id INTEGER, occurred_at TIMESTAMP);
INSERT INTO events VALUES
  (1, '2025-01-05 08:30:00'),
  (2, '2025-01-28 14:00:00'),
  (3, '2025-02-14 09:15:00'),
  (4, '2025-03-01 00:00:00');`,
  subscriptions1: `CREATE OR REPLACE TABLE subscriptions (subscription_id INTEGER, started_at DATE, cancelled_at DATE);
INSERT INTO subscriptions VALUES
  (1, '2025-01-01', '2025-01-11'),
  (2, '2025-02-01', '2025-02-05'),
  (3, '2025-03-01', '2025-03-31'),
  (4, '2025-04-10', '2025-04-12');`,
  orders1: `CREATE OR REPLACE TABLE orders (order_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, '2025-01-05', 50.00),
  (2, '2025-01-20', 30.00),
  (3, '2025-02-02', 45.00),
  (4, '2025-02-25', 15.00),
  (5, '2025-03-10', 60.00);`,
  orders2: `CREATE OR REPLACE TABLE orders (order_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, '2024-04-03', 20.00),
  (2, '2025-03-15', 40.00),
  (3, '2025-04-18', 35.00),
  (4, '2025-05-01', 10.00),
  (5, '2023-04-30', 25.00);`,
  webinarAttendeesEmailClickers: `CREATE OR REPLACE TABLE webinar_attendees (customer_id INTEGER);
INSERT INTO webinar_attendees VALUES (1), (2), (3), (4);
CREATE OR REPLACE TABLE email_clickers (customer_id INTEGER);
INSERT INTO email_clickers VALUES (2), (3), (5), (6);`,
  activeCustomersFeedbackSubmitters: `CREATE OR REPLACE TABLE active_customers (customer_id INTEGER);
INSERT INTO active_customers VALUES (1), (2), (3), (4), (5);
CREATE OR REPLACE TABLE feedback_submitters (customer_id INTEGER);
INSERT INTO feedback_submitters VALUES (2), (4);`,
  orders3: `CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 10.00),
  (2, 2, 50.00),
  (3, 3, 20.00),
  (4, 1, 90.00),
  (5, 2, 30.00);`,
  ordersCustomers: `CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 10.00),
  (2, 2, 50.00),
  (3, 3, 20.00),
  (4, 1, 90.00);
CREATE OR REPLACE TABLE customers (customer_id INTEGER, region VARCHAR);
INSERT INTO customers VALUES
  (1, 'west'),
  (2, 'east'),
  (3, 'west');`,
  customersOrders2: `CREATE OR REPLACE TABLE customers (customer_id INTEGER, region VARCHAR);
INSERT INTO customers VALUES
  (1, 'west'),
  (2, 'east'),
  (3, 'west'),
  (4, 'west');
CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 10.00),
  (2, 2, 50.00);`,
  sourceAccountsSourceSubscriptions: `
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
`,
  eventsSubscriptionHistory: `
CREATE OR REPLACE TABLE events (
    event_id INTEGER, user_id INTEGER, event_type VARCHAR, event_ts TIMESTAMP, session_id VARCHAR
);
INSERT INTO events VALUES
 (1,1,'login','2024-01-01 08:00:00','s1'),
 (2,1,'view_page','2024-01-01 08:05:00','s1'),
 (3,1,'login','2024-01-02 09:00:00','s2'),
 (4,2,'login','2024-01-01 10:00:00','s3'),
 (5,2,'purchase','2024-01-01 10:15:00','s3'),
 (6,2,'login','2024-01-03 11:00:00','s4'),
 (7,3,'login','2024-01-01 12:00:00','s5');

CREATE OR REPLACE TABLE subscription_history (
    sub_id INTEGER, account_id INTEGER, status VARCHAR, effective_date DATE
);
INSERT INTO subscription_history VALUES
 (1,1,'trial','2023-01-01'),
 (1,1,'active','2023-02-01'),
 (1,1,'active','2023-03-01'),
 (1,1,'churned','2023-04-01'),
 (2,2,'active','2023-01-01');
`,
  accountsPlanAccounts: `
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
`,
  payments: `CREATE OR REPLACE TABLE payments (payment_id INTEGER, account_id INTEGER, paid_at DATE, amount DECIMAL(10,2));
INSERT INTO payments VALUES
  (1, 1, '2025-01-01', 10.00),
  (2, 1, '2025-02-01', 20.00),
  (3, 1, '2025-03-01', 15.00),
  (4, 2, '2025-01-10', 5.00),
  (5, 2, '2025-02-10', 25.00);`,
  dailySignups: `CREATE OR REPLACE TABLE daily_signups (signup_date DATE, signup_count INTEGER);
INSERT INTO daily_signups VALUES
  ('2025-01-01', 10),
  ('2025-01-02', 20),
  ('2025-01-03', 30),
  ('2025-01-04', 15),
  ('2025-01-05', 25);`,
  customers2: `CREATE OR REPLACE TABLE customers (customer_id INTEGER, lifetime_value DECIMAL(10,2));
INSERT INTO customers VALUES
  (1, 100.00),
  (2, 400.00),
  (3, 250.00),
  (4, 50.00),
  (5, 300.00),
  (6, 150.00),
  (7, 500.00),
  (8, 75.00);`,
  orders4: `CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, '2025-01-01', 10.00),
  (2, 1, '2025-02-01', 20.00),
  (3, 1, '2025-03-01', 30.00),
  (4, 2, '2025-01-15', 5.00),
  (5, 2, '2025-02-15', 15.00);`,
  payments1: `CREATE OR REPLACE TABLE payments (payment_id INTEGER, account_id INTEGER, paid_at DATE, amount DECIMAL(10,2));
INSERT INTO payments VALUES
  (1, 1, '2025-01-01', 10.00),
  (2, 1, '2025-02-01', 20.00),
  (3, 1, '2025-03-01', 15.00),
  (4, 2, '2025-01-10', 5.00),
  (5, 2, '2025-02-10', 25.00),
  (6, 2, '2025-03-10', 35.00);`,
  employees1: `CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', NULL),
  (2, 'Sam', 1),
  (3, 'Lee', 1),
  (4, 'Noor', 2),
  (5, 'Kai', 2);`,
  productCatalogInventory: `CREATE OR REPLACE TABLE product_catalog (product_id INTEGER, product_name VARCHAR);
INSERT INTO product_catalog VALUES
  (1, 'Widget'),
  (2, 'Gadget'),
  (3, 'Gizmo');
CREATE OR REPLACE TABLE inventory (product_id INTEGER, quantity_on_hand INTEGER);
INSERT INTO inventory VALUES
  (2, 40),
  (3, 10),
  (4, 5);`,
  shipmentsWarehouseRates: `CREATE OR REPLACE TABLE shipments (shipment_id INTEGER, warehouse_code VARCHAR, order_id INTEGER, shipped_at DATE);
INSERT INTO shipments VALUES
  (1, 'WH1', 100, '2024-06-01'),
  (2, 'WH1', 101, '2025-06-01'),
  (3, 'WH2', 102, '2025-01-15');
CREATE OR REPLACE TABLE warehouse_rates (warehouse_code VARCHAR, effective_year INTEGER, rate_per_unit DECIMAL(10,2));
INSERT INTO warehouse_rates VALUES
  ('WH1', 2024, 1.50),
  ('WH1', 2025, 1.75),
  ('WH2', 2025, 2.00);`,
  employees2: `CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, department VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', 'eng', NULL),
  (2, 'Sam', 'eng', 1),
  (3, 'Lee', 'eng', 1),
  (4, 'Noor', 'eng', 1),
  (5, 'Kai', 'sales', 1);`,
  employeesPayrollRecords: `CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', NULL),
  (2, 'Sam', 1),
  (3, 'Lee', 1);
CREATE OR REPLACE TABLE payroll_records (employee_id INTEGER, salary DECIMAL(10,2));
INSERT INTO payroll_records VALUES
  (1, 150000.00),
  (2, 110000.00),
  (9, 95000.00);`,
  subscriptions2: `CREATE OR REPLACE TABLE subscriptions (subscription_id INTEGER, status VARCHAR);
INSERT INTO subscriptions VALUES
  (1, 'active'),
  (2, 'trialing'),
  (3, 'pending'),
  (4, 'cancelled'),
  (5, 'archived');`,
  priceHistory: `CREATE OR REPLACE TABLE price_history (product_id INTEGER, effective_date DATE, price DECIMAL(10,2));
INSERT INTO price_history VALUES
  (1, '2025-01-01', 9.99),
  (1, '2025-01-01', 10.99),
  (1, '2025-02-01', 11.99),
  (2, '2025-01-01', 19.99),
  (2, '2025-01-01', 19.99);`,
  ordersStatusLookup: `CREATE OR REPLACE TABLE orders (order_id INTEGER, status_code VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 'A', 10.00),
  (2, 'B', 20.00),
  (3, 'A', 15.00),
  (4, 'C', 5.00);
CREATE OR REPLACE TABLE status_lookup (status_code VARCHAR, status_label VARCHAR);
INSERT INTO status_lookup VALUES
  ('A', 'Open'),
  ('B', 'Shipped'),
  ('C', 'Cancelled');`,
  ordersCustomers1: `CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER);
INSERT INTO orders VALUES
  (1, 1),
  (2, NULL),
  (3, 2),
  (4, 99);
CREATE OR REPLACE TABLE customers (customer_id INTEGER);
INSERT INTO customers VALUES (1), (2), (3);`,
  ordersStatusLookup1: `CREATE OR REPLACE TABLE orders (order_id INTEGER, status_code VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 'A', 10.00),
  (2, 'B', 20.00),
  (3, 'Z', 15.00),
  (4, 'C', 5.00);
CREATE OR REPLACE TABLE status_lookup (status_code VARCHAR, status_label VARCHAR, is_valid_status BOOLEAN);
INSERT INTO status_lookup VALUES
  ('A', 'Open', true),
  ('B', 'Shipped', true),
  ('C', 'Retired', false);`,
  existingTargetRawUsageEvents: `
CREATE OR REPLACE TABLE existing_target (
    event_id INTEGER, account_id INTEGER, event_type VARCHAR, event_date DATE, loaded_at TIMESTAMP
);
INSERT INTO existing_target VALUES
 (1,1,'login','2024-01-01','2024-01-01 00:05:00'),
 (2,2,'login','2024-01-01','2024-01-01 00:06:00');

CREATE OR REPLACE TABLE raw_usage_events (
    event_id INTEGER, account_id INTEGER, event_type VARCHAR, event_date DATE, loaded_at TIMESTAMP
);
INSERT INTO raw_usage_events VALUES
 (1,1,'login_updated','2024-01-01','2024-01-05 00:00:00'),
 (2,2,'login','2024-01-01','2024-01-01 00:06:00'),
 (3,1,'purchase','2024-01-10','2024-01-10 00:00:00'),
 (4,3,'login','2024-01-11','2024-01-11 00:00:00'),
 (5,3,'purchase','2024-01-12','2024-01-12 00:00:00');
`,
  rawPayloads: `
CREATE OR REPLACE TABLE raw_payloads (id INTEGER, account_id INTEGER, payload VARCHAR);
INSERT INTO raw_payloads VALUES
 (1,1,'{"plan":"enterprise","teams":[{"team_id":10,"seats":5},{"team_id":11,"seats":3}],"features":["sso","reporting"]}'),
 (2,2,'{"plan":"growth","teams":[{"team_id":20,"seats":2}],"features":["reporting"]}'),
 (3,3,'{"plan":"starter","teams":[],"features":[]}');
`,
  dailyFeedDay1DailyFeedDay2: `
CREATE OR REPLACE TABLE daily_feed_day1 (employee_id INTEGER, department VARCHAR, salary DECIMAL(10,2));
INSERT INTO daily_feed_day1 VALUES (1,'engineering',90000),(2,'sales',70000),(3,'marketing',65000);

CREATE OR REPLACE TABLE daily_feed_day2 (employee_id INTEGER, department VARCHAR, salary DECIMAL(10,2));
INSERT INTO daily_feed_day2 VALUES (1,'engineering',95000),(2,'sales',70000),(4,'engineering',80000);

CREATE OR REPLACE TABLE employee_history (employee_id INTEGER, department VARCHAR, salary DECIMAL(10,2), valid_from DATE);
INSERT INTO employee_history VALUES
 (1,'engineering',90000,'2023-01-01'),
 (1,'engineering',95000,'2023-06-01'),
 (2,'sales',70000,'2023-01-01');
`,
  sourceASourceB: `
CREATE OR REPLACE TABLE source_a (id INTEGER, name VARCHAR, amount DECIMAL(10,2), created_at TIMESTAMP);
INSERT INTO source_a VALUES (1,'Acme',100.00,'2024-01-01 00:00:00'),(2,'Globex',200.00,'2024-01-02 00:00:00');

CREATE OR REPLACE TABLE source_b (id INTEGER, name VARCHAR, amount_usd VARCHAR, created_ts TIMESTAMP);
INSERT INTO source_b VALUES (2,'Globex Updated','250.00','2024-02-01 00:00:00'),(3,'Initech','300.00','2024-01-03 00:00:00');

CREATE OR REPLACE TABLE columns_metadata (column_name VARCHAR, data_type VARCHAR);
INSERT INTO columns_metadata VALUES
 ('id','INTEGER'),('name','VARCHAR'),('amount','DECIMAL'),('created_at','TIMESTAMP_TZ'),('updated_at','TIMESTAMP_TZ'),('region','VARCHAR');
`,
  accountsMultiTerritoryPlan: `
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
`,
  employees3: `CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', NULL),
  (2, 'Sam', 1),
  (3, 'Lee', 1),
  (4, 'Noor', 2),
  (5, 'Kai', 4);`,
  employees4: `CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', NULL),
  (2, 'Sam', 1),
  (3, 'Lee', 1),
  (4, 'Noor', 2);`,
  customers3: `CREATE OR REPLACE TABLE customers (customer_id INTEGER, first_name VARCHAR, last_name VARCHAR, email VARCHAR);
INSERT INTO customers VALUES
  (1, 'Ana', 'Lopez', 'ana@example.com'),
  (2, 'Ben', 'Kim', 'ben@example.com'),
  (3, 'Cara', 'Diaz', 'cara@example.com');`,
  orders5: `CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2), status VARCHAR);
INSERT INTO orders VALUES
  (1, 100, 25.50, 'shipped'),
  (2, 101, 10.00, 'pending'),
  (3, 102, 40.25, 'shipped');`,
  orderItems: `CREATE OR REPLACE TABLE order_items (order_id INTEGER, product_name VARCHAR, quantity INTEGER);
INSERT INTO order_items VALUES
  (1, 'Widget', 2),
  (1, 'Gadget', 1),
  (2, 'Gizmo', 5),
  (2, 'Widget', 3),
  (2, 'Gadget', 4);`,
  orderItems1: `CREATE OR REPLACE TABLE order_items (order_id INTEGER, product_name VARCHAR, quantity INTEGER);
INSERT INTO order_items VALUES
  (1, 'Widget', 2),
  (1, 'Gadget', 1),
  (2, 'Gizmo', 5),
  (2, 'Widget', 3);`,
  customersOrders3: `CREATE OR REPLACE TABLE customers (customer_id INTEGER, customer_name VARCHAR);
INSERT INTO customers VALUES
  (1, 'Ana Lopez'),
  (2, 'Ben Kim');
CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (10, 1, 25.00),
  (11, 1, 40.00),
  (12, 2, 15.00);`,
  orders6: `CREATE OR REPLACE TABLE orders (order_id INTEGER, region VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 'west', 10.00),
  (2, 'east', 20.00),
  (3, 'west', 15.00),
  (4, 'north', 5.00),
  (5, 'east', 25.00);`,
  orders7: `CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, channel VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 'online', 10.00),
  (2, 1, 'retail', 20.00),
  (3, 2, 'online', 15.00),
  (4, 2, 'online', 5.00),
  (5, 3, 'retail', 30.00);`,
  dailySales: `CREATE OR REPLACE TABLE daily_sales (sale_date DATE, region VARCHAR, amount DECIMAL(10,2));
INSERT INTO daily_sales VALUES
  ('2025-01-01', 'west', 10.00),
  ('2025-01-02', 'west', 20.00),
  ('2025-01-03', 'west', 30.00),
  ('2025-01-04', 'west', 5.00),
  ('2025-01-01', 'east', 100.00),
  ('2025-01-02', 'east', 50.00);`,
  dailySales1: `CREATE OR REPLACE TABLE daily_sales (sale_date DATE, channel VARCHAR, amount DECIMAL(10,2));
INSERT INTO daily_sales VALUES
  ('2025-01-01', 'online', 10.00),
  ('2025-01-01', 'retail', 5.00),
  ('2025-01-02', 'online', 20.00),
  ('2025-01-02', 'retail', 8.00),
  ('2025-01-03', 'online', 30.00),
  ('2025-01-03', 'retail', 12.00),
  ('2025-01-04', 'online', 5.00),
  ('2025-01-04', 'retail', 3.00);`,
};

const MODULES = [
  {
    "id": "1.1",
    "lesson": 1,
    "difficulty": "easy",
    "title": "Select, filter, and sort",
    "concept": "SELECT / WHERE / ORDER BY",
    "tables": "customers(customer_id, first_name, last_name, region, signup_date, is_active)",
    "prompt": "Write a query against `customers` that returns `first_name`, `last_name`, and `region` for every customer in the 'west' region.\n\nOrder the results alphabetically by `last_name`.",
    "schemaSql": SCHEMAS.customersOrders,
    "solutionSql": "SELECT first_name, last_name, region FROM customers WHERE region = 'west' ORDER BY last_name;",
    "hint": "A basic WHERE clause on region, then ORDER BY last_name.",
    "starter": "-- customers(customer_id, first_name, last_name, region, signup_date, is_active)\n",
  },
  {
    "id": "1.2",
    "lesson": 1,
    "difficulty": "easy",
    "title": "Style conventions: != and AND",
    "concept": "!= over <>, compound WHERE",
    "tables": "customers(customer_id, first_name, last_name, region, signup_date, is_active)",
    "prompt": "This repo's SQL style guide prefers `!=` over `<>` for \"not equal\".\n\nReturn `customer_id`, `first_name`, and `signup_date` for customers whose `region` is not 'west' AND who signed up on or after 2023-01-01.\n\nOrder by `signup_date`.",
    "schemaSql": SCHEMAS.customersOrders,
    "solutionSql": "SELECT customer_id, first_name, signup_date FROM customers WHERE region != 'west' AND signup_date >= DATE '2023-01-01' ORDER BY signup_date;",
    "hint": "Use != instead of <>, and combine two conditions with AND. Try DATE '2023-01-01' for the date literal.",
    "starter": "-- customers(customer_id, first_name, last_name, region, signup_date, is_active)\n",
  },
  {
    "id": "1.3",
    "lesson": 1,
    "difficulty": "easy",
    "title": "Aliasing and Snowflake-style casts",
    "concept": "::type casts, explicit aliases",
    "tables": "orders(order_id, customer_id, order_date, amount, status)",
    "prompt": "This codebase leans heavily on Snowflake's `::type` shorthand instead of `CAST(x AS type)`.\n\nFrom `orders`, return `order_id`, the `amount` cast to an integer (rounded to the nearest dollar) aliased as `amount_whole_dollars`, and `order_date` cast to a string aliased as `order_date_string`.\n\nOrder by `order_id`.",
    "schemaSql": SCHEMAS.customersOrders,
    "solutionSql": "SELECT order_id, amount::INTEGER AS amount_whole_dollars, order_date::VARCHAR AS order_date_string FROM orders ORDER BY order_id;",
    "hint": "amount::INTEGER and order_date::VARCHAR, each with an explicit AS alias.",
    "starter": "-- orders(order_id, customer_id, order_date, amount, status)\n",
  },
  {
    "id": "1.4",
    "lesson": 1,
    "difficulty": "easy",
    "title": "CASE WHEN tiers",
    "concept": "CASE WHEN ... ELSE ... END",
    "tables": "orders(order_id, customer_id, order_date, amount, status)",
    "prompt": "Add a computed column `business_tier` to `orders` that labels each order:\n- 'large' when amount >= 100\n- 'medium' when amount >= 50\n- otherwise 'small'\n\nReturn `order_id`, `amount`, `business_tier`, ordered by `order_id`.",
    "schemaSql": SCHEMAS.customersOrders,
    "solutionSql": "SELECT order_id, amount, CASE WHEN amount >= 100 THEN 'large' WHEN amount >= 50 THEN 'medium' ELSE 'small' END AS business_tier FROM orders ORDER BY order_id;",
    "hint": "CASE WHEN amount >= 100 THEN ... WHEN amount >= 50 THEN ... ELSE ... END AS business_tier",
    "starter": "-- orders(order_id, customer_id, order_date, amount, status)\n",
  },
  {
    "id": "1.5",
    "lesson": 1,
    "difficulty": "easy",
    "title": "Distinct values",
    "concept": "SELECT DISTINCT",
    "tables": "customers(customer_id, first_name, last_name, region, signup_date, is_active)",
    "prompt": "Return the distinct list of `region` values represented in `customers`, ordered alphabetically.",
    "schemaSql": SCHEMAS.customersOrders,
    "solutionSql": "SELECT DISTINCT region FROM customers ORDER BY region;",
    "hint": "SELECT DISTINCT region ... ORDER BY region.",
    "starter": "-- customers(customer_id, first_name, last_name, region, signup_date, is_active)\n",
  },
  {
    "id": "2.1",
    "lesson": 2,
    "difficulty": "easy",
    "title": "Basic join",
    "concept": "JOIN ... ON",
    "tables": "customers(customer_id, first_name, last_name, region, signup_date, is_active, referral_source)\norders(order_id, customer_id, order_date, amount, status)",
    "prompt": "Join `customers` to `orders` and return each customer's `first_name`, `last_name`, plus the `order_id` and `amount` for every order with status = 'completed'.\n\nOrder by `customer_id`, then `order_id`.",
    "schemaSql": SCHEMAS.customersOrders1,
    "solutionSql": "SELECT c.first_name, c.last_name, o.order_id, o.amount FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'completed' ORDER BY c.customer_id, o.order_id;",
    "hint": "JOIN orders o ON c.customer_id = o.customer_id, then filter on o.status.",
    "starter": "-- customers(customer_id, first_name, last_name, region, ...)\n-- orders(order_id, customer_id, order_date, amount, status)\n",
  },
  {
    "id": "2.2",
    "lesson": 2,
    "difficulty": "easy",
    "title": "Anti-join with LEFT JOIN",
    "concept": "LEFT JOIN + IS NULL",
    "tables": "customers(customer_id, first_name, ...)\norders(order_id, customer_id, ...)",
    "prompt": "Return the `customer_id` and `first_name` of customers who have never placed an order (they don't appear in orders at all).\n\nOrder by `customer_id`.",
    "schemaSql": SCHEMAS.customersOrders1,
    "solutionSql": "SELECT c.customer_id, c.first_name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL ORDER BY c.customer_id;",
    "hint": "LEFT JOIN orders, then filter WHERE o.order_id IS NULL to find rows with no match.",
    "starter": "-- customers(customer_id, first_name, ...)\n-- orders(order_id, customer_id, ...)\n",
  },
  {
    "id": "2.3",
    "lesson": 2,
    "difficulty": "easy",
    "title": "GROUP BY with HAVING",
    "concept": "GROUP BY / SUM / HAVING",
    "tables": "orders(order_id, customer_id, order_date, amount, status)",
    "prompt": "For each `customer_id`, return the total `amount` spent across completed orders only, aliased `total_spent`.\n\nOnly include customers whose `total_spent` exceeds 40.\n\nOrder by `total_spent` descending.",
    "schemaSql": SCHEMAS.customersOrders1,
    "solutionSql": "SELECT customer_id, SUM(amount) AS total_spent FROM orders WHERE status='completed' GROUP BY customer_id HAVING SUM(amount) > 40 ORDER BY total_spent DESC;",
    "hint": "Filter WHERE status = 'completed' before grouping, then GROUP BY customer_id HAVING SUM(amount) > 40.",
    "starter": "-- orders(order_id, customer_id, order_date, amount, status)\n",
  },
  {
    "id": "2.4",
    "lesson": 2,
    "difficulty": "easy",
    "title": "Defaulting nulls with COALESCE",
    "concept": "COALESCE / IFNULL fallback",
    "tables": "customers(customer_id, first_name, ..., referral_source)",
    "prompt": "Some customers have a null `referral_source`. Return `customer_id`, `first_name`, and `referral_source` defaulted to 'organic' when null (alias it `referral_source_final`).\n\nOrder by `customer_id`.",
    "schemaSql": SCHEMAS.customersOrders1,
    "solutionSql": "SELECT customer_id, first_name, COALESCE(referral_source, 'organic') AS referral_source_final FROM customers ORDER BY customer_id;",
    "hint": "COALESCE(referral_source, 'organic') AS referral_source_final",
    "starter": "-- customers(customer_id, first_name, ..., referral_source)\n",
  },
  {
    "id": "2.5",
    "lesson": 2,
    "difficulty": "easy",
    "title": "Capstone: join + case + aggregate",
    "concept": "LEFT JOIN + conditional aggregation",
    "tables": "customers(customer_id, ..., region)\norders(order_id, customer_id, amount, status)",
    "prompt": "Return, for each `region`: the count of distinct customers (`customer_count`) and the total completed order amount for that region, aliased `total_completed_amount`, defaulting to 0 when a region has no completed orders.\n\nOrder by `total_completed_amount` descending.",
    "schemaSql": SCHEMAS.customersOrders1,
    "solutionSql": "SELECT c.region,\n       COUNT(DISTINCT c.customer_id) AS customer_count,\n       COALESCE(SUM(CASE WHEN o.status='completed' THEN o.amount END),0) AS total_completed_amount\nFROM customers c\nLEFT JOIN orders o ON c.customer_id = o.customer_id\nGROUP BY c.region\nORDER BY total_completed_amount DESC;",
    "hint": "LEFT JOIN customers to orders, GROUP BY region, and use SUM(CASE WHEN status='completed' THEN amount END) wrapped in COALESCE.",
    "starter": "-- customers(customer_id, ..., region)\n-- orders(order_id, customer_id, amount, status)\n",
  },
  {
    "id": "3.1",
    "lesson": 3,
    "difficulty": "easy",
    "title": "Normalize Case with UPPER/LOWER",
    "concept": "UPPER/LOWER",
    "tables": "customers(customer_id, first_name, email)",
    "prompt": "The `customers` table has emails stored with inconsistent casing. Return `customer_id`, `first_name`, and the email lowercased as `email_clean`. Order by `customer_id`.",
    "schemaSql": SCHEMAS.customers,
    "solutionSql": "select\n    customer_id\n  , first_name\n  , lower(email) as email_clean\nfrom customers\norder by customer_id",
    "hint": "Wrap the `email` column in `lower(...)` and alias it `email_clean`.",
    "starter": "-- customers(customer_id, first_name, email)\n",
  },
  {
    "id": "3.2",
    "lesson": 3,
    "difficulty": "easy",
    "title": "Clean Up Whitespace with TRIM",
    "concept": "TRIM",
    "tables": "customers(customer_id, raw_name)",
    "prompt": "`customers.raw_name` was loaded from a messy CSV export and has leading/trailing spaces. Return `customer_id` and `raw_name` trimmed as `clean_name`. Order by `customer_id`.",
    "schemaSql": SCHEMAS.customers1,
    "solutionSql": "select\n    customer_id\n  , trim(raw_name) as clean_name\nfrom customers\norder by customer_id",
    "hint": "`trim(raw_name)` strips leading and trailing whitespace; alias it `clean_name`.",
    "starter": "-- customers(customer_id, raw_name)\n",
  },
  {
    "id": "3.3",
    "lesson": 3,
    "difficulty": "easy",
    "title": "Build Full Names with CONCAT & LENGTH",
    "concept": "CONCAT/LENGTH",
    "tables": "employees(employee_id, first_name, last_name)",
    "prompt": "Return `employee_id`, a `full_name` built by concatenating `first_name`, a single space, and `last_name`, and the character count of that full name as `name_length`.\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.employees,
    "solutionSql": "select\n    employee_id\n  , concat(first_name, ' ', last_name) as full_name\n  , length(concat(first_name, ' ', last_name)) as name_length\nfrom employees\norder by employee_id",
    "hint": "`concat(first_name, ' ', last_name)` for the name, then wrap that same expression in `length(...)`.",
    "starter": "-- employees(employee_id, first_name, last_name)\n",
  },
  {
    "id": "3.4",
    "lesson": 3,
    "difficulty": "easy",
    "title": "Pull Codes Out with SUBSTRING",
    "concept": "SUBSTRING",
    "tables": "products(product_id, sku)",
    "prompt": "Every `sku` starts with a 4-character category code, e.g. `'ELEC-1001'` -> `'ELEC'`. Return `product_id`, `sku`, and the first 4 characters of `sku` as `category_code`.\n\nOrder by `product_id`.",
    "schemaSql": SCHEMAS.products,
    "solutionSql": "select\n    product_id\n  , sku\n  , substring(sku, 1, 4) as category_code\nfrom products\norder by product_id",
    "hint": "`substring(sku, 1, 4)` takes 4 characters starting at position 1.",
    "starter": "-- products(product_id, sku)\n",
  },
  {
    "id": "3.5",
    "lesson": 3,
    "difficulty": "easy",
    "title": "Redact Placeholder Text with REPLACE",
    "concept": "REPLACE",
    "tables": "support_tickets(ticket_id, description)",
    "prompt": "Support ticket templates use a literal `{{customer}}` placeholder that never got filled in. Return `ticket_id` and a cleaned `description` where every `{{customer}}` token is replaced with the word `the customer`, then uppercased.\n\nOrder by `ticket_id`.",
    "schemaSql": SCHEMAS.supportTickets,
    "solutionSql": "select\n    ticket_id\n  , upper(replace(description, '{{customer}}', 'the customer')) as description\nfrom support_tickets\norder by ticket_id",
    "hint": "Nest the calls: `upper(replace(description, '{{customer}}', 'the customer'))`.",
    "starter": "-- support_tickets(ticket_id, description)\n",
  },
  {
    "id": "4.1",
    "lesson": 4,
    "difficulty": "easy",
    "title": "Finding Missing Values",
    "concept": "IS NULL / IS NOT NULL",
    "tables": "accounts(account_id, plan_name, cancelled_at)",
    "prompt": "In `accounts`, an account is considered still active when it has no cancellation recorded. Return the `account_id` and `plan_name` of every account that is still active. Order by `account_id`.",
    "schemaSql": SCHEMAS.accounts,
    "solutionSql": "select\n    account_id\n  , plan_name\nfrom accounts\nwhere cancelled_at is null\norder by account_id",
    "hint": "Filter with `where cancelled_at is null` -- never `= null`, which always evaluates to unknown.",
    "starter": "-- accounts(account_id, plan_name, cancelled_at)\n",
  },
  {
    "id": "4.2",
    "lesson": 4,
    "difficulty": "easy",
    "title": "Guarding Against Divide-by-Zero with NULLIF",
    "concept": "NULLIF",
    "tables": "campaigns(campaign_id, clicks, impressions)",
    "prompt": "Some campaigns have zero impressions, which would blow up a naive click-through-rate calculation (division by zero). Return `campaign_id` and a computed `ctr` column (clicks divided by impressions) that safely comes back as null instead of erroring when impressions is zero. Order by `campaign_id`.",
    "schemaSql": SCHEMAS.campaigns,
    "solutionSql": "select\n    campaign_id\n  , clicks / nullif(impressions, 0) as ctr\nfrom campaigns\norder by campaign_id",
    "hint": "`nullif(impressions, 0)` turns a 0 into null, so dividing by it yields null instead of an error.",
    "starter": "-- campaigns(campaign_id, clicks, impressions)\n",
  },
  {
    "id": "4.3",
    "lesson": 4,
    "difficulty": "easy",
    "title": "Combining Conditions with AND/OR/NOT",
    "concept": "AND/OR/NOT",
    "tables": "subscriptions(subscription_id, plan_name, status, is_trial)",
    "prompt": "Return every `subscription_id`, `plan_name`, and `status` where the subscription is `active` AND NOT a trial, OR the plan is `enterprise` regardless of trial status.\n\nOrder by `subscription_id`.",
    "schemaSql": SCHEMAS.subscriptions,
    "solutionSql": "select\n    subscription_id\n  , plan_name\n  , status\nfrom subscriptions\nwhere (status = 'active' and not is_trial)\n   or plan_name = 'enterprise'\norder by subscription_id",
    "hint": "Group the first condition in parentheses: `(status = 'active' and not is_trial) or plan_name = 'enterprise'`.",
    "starter": "-- subscriptions(subscription_id, plan_name, status, is_trial)\n",
  },
  {
    "id": "4.4",
    "lesson": 4,
    "difficulty": "easy",
    "title": "Filtering Lists with IN / NOT IN",
    "concept": "IN / NOT IN",
    "tables": "events(event_id, event_type)",
    "prompt": "Return the `event_id` and `event_type` for every event whose `event_type` is one of `'signup'`, `'upgrade'`, or `'renewal'`, excluding anything else. Order by `event_id`.",
    "schemaSql": SCHEMAS.events,
    "solutionSql": "select\n    event_id\n  , event_type\nfrom events\nwhere event_type in ('signup', 'upgrade', 'renewal')\norder by event_id",
    "hint": "`where event_type in ('signup', 'upgrade', 'renewal')`.",
    "starter": "-- events(event_id, event_type)\n",
  },
  {
    "id": "4.5",
    "lesson": 4,
    "difficulty": "easy",
    "title": "Combining NULL Handling with Boolean Logic",
    "concept": "COALESCE + AND/OR + IS NULL",
    "tables": "leads(lead_id, source, converted_at, is_qualified)",
    "prompt": "Return `lead_id`, `source`, and a `converted_flag` boolean that is true when the lead has actually converted AND is qualified, OR when the lead's `source` is `'referral'` (referrals always count regardless of qualification). Some `is_qualified` values are null and should be treated as not-qualified rather than unknown. Order by `lead_id`.",
    "schemaSql": SCHEMAS.leads,
    "solutionSql": "select\n    lead_id\n  , source\n  , (converted_at is not null and coalesce(is_qualified, false)) or source = 'referral' as converted_flag\nfrom leads\norder by lead_id",
    "hint": "Combine `(converted_at is not null and coalesce(is_qualified, false))` with `or source = 'referral'`.",
    "starter": "-- leads(lead_id, source, converted_at, is_qualified)\n",
  },
  {
    "id": "5.1",
    "lesson": 5,
    "difficulty": "easy",
    "title": "Pulling Date Parts with EXTRACT",
    "concept": "EXTRACT(part FROM date)",
    "tables": "orders(order_id, order_date)",
    "prompt": "Return `order_id`, and the calendar year and month extracted from `order_date`, aliased `order_year` and `order_month`. Order by `order_id`.",
    "schemaSql": SCHEMAS.orders,
    "solutionSql": "select\n    order_id\n  , extract(year from order_date) as order_year\n  , extract(month from order_date) as order_month\nfrom orders\norder by order_id",
    "hint": "`extract(year from order_date)` and `extract(month from order_date)`.",
    "starter": "-- orders(order_id, order_date)\n",
  },
  {
    "id": "5.2",
    "lesson": 5,
    "difficulty": "easy",
    "title": "Rounding Timestamps with DATE_TRUNC",
    "concept": "DATE_TRUNC",
    "tables": "events(event_id, occurred_at)",
    "prompt": "Return `event_id` and `occurred_at` truncated down to the start of its calendar month, aliased `event_month`. Order by `event_id`.",
    "schemaSql": SCHEMAS.events1,
    "solutionSql": "select\n    event_id\n  , date_trunc('month', occurred_at) as event_month\nfrom events\norder by event_id",
    "hint": "`date_trunc('month', occurred_at)` zeroes out the day/time down to the 1st of the month.",
    "starter": "-- events(event_id, occurred_at)\n",
  },
  {
    "id": "5.3",
    "lesson": 5,
    "difficulty": "easy",
    "title": "Counting Days Between Dates",
    "concept": "date subtraction",
    "tables": "subscriptions(subscription_id, started_at, cancelled_at)",
    "prompt": "Return `subscription_id` and the number of days each subscription was active, aliased `days_active`.\n\nOrder by `subscription_id`.",
    "schemaSql": SCHEMAS.subscriptions1,
    "solutionSql": "select\n    subscription_id\n  , cancelled_at - started_at as days_active\nfrom subscriptions\norder by subscription_id",
    "hint": "Two `date` columns subtract directly into a day count: `cancelled_at - started_at`.",
    "starter": "-- subscriptions(subscription_id, started_at, cancelled_at)\n",
  },
  {
    "id": "5.4",
    "lesson": 5,
    "difficulty": "easy",
    "title": "Grouping by Month with DATE_TRUNC",
    "concept": "DATE_TRUNC + GROUP BY",
    "tables": "orders(order_id, order_date, amount)",
    "prompt": "Return one row per calendar month, aliased `order_month`, with the total `amount` for that month as `total_amount`.\n\nOrder by `order_month`.",
    "schemaSql": SCHEMAS.orders1,
    "solutionSql": "select\n    date_trunc('month', order_date) as order_month\n  , sum(amount) as total_amount\nfrom orders\ngroup by date_trunc('month', order_date)\norder by order_month",
    "hint": "Group by the same `date_trunc('month', order_date)` expression you select, then `sum(amount)`.",
    "starter": "-- orders(order_id, order_date, amount)\n",
  },
  {
    "id": "5.5",
    "lesson": 5,
    "difficulty": "easy",
    "title": "Filtering on Extracted Date Parts",
    "concept": "EXTRACT + WHERE",
    "tables": "orders(order_id, order_date, amount)",
    "prompt": "Return `order_id`, `order_date`, and `amount` for orders placed in April, regardless of year. Order by `order_date`.",
    "schemaSql": SCHEMAS.orders2,
    "solutionSql": "select\n    order_id\n  , order_date\n  , amount\nfrom orders\nwhere extract(month from order_date) = 4\norder by order_date",
    "hint": "Filter with `where extract(month from order_date) = 4` -- no year comparison needed.",
    "starter": "-- orders(order_id, order_date, amount)\n",
  },
  {
    "id": "6.1",
    "lesson": 6,
    "difficulty": "easy",
    "title": "Finding Overlap with INTERSECT",
    "concept": "INTERSECT",
    "tables": "webinar_attendees(customer_id)\nemail_clickers(customer_id)",
    "prompt": "Return the `customer_id`s that appear in BOTH `webinar_attendees` AND `email_clickers`. Order by `customer_id`.",
    "schemaSql": SCHEMAS.webinarAttendeesEmailClickers,
    "solutionSql": "select customer_id from webinar_attendees\nintersect\nselect customer_id from email_clickers\norder by customer_id",
    "hint": "`select customer_id from webinar_attendees intersect select customer_id from email_clickers`.",
    "starter": "-- webinar_attendees(customer_id)\n  -- email_clickers(customer_id)\n",
  },
  {
    "id": "6.2",
    "lesson": 6,
    "difficulty": "easy",
    "title": "Finding Differences with EXCEPT",
    "concept": "EXCEPT",
    "tables": "active_customers(customer_id)\nfeedback_submitters(customer_id)",
    "prompt": "Return the `customer_id`s that are in `active_customers` but have never submitted feedback (i.e. don't appear in `feedback_submitters`). Order by `customer_id`.",
    "schemaSql": SCHEMAS.activeCustomersFeedbackSubmitters,
    "solutionSql": "select customer_id from active_customers\nexcept\nselect customer_id from feedback_submitters\norder by customer_id",
    "hint": "`select ... from active_customers except select ... from feedback_submitters`.",
    "starter": "-- active_customers(customer_id)\n  -- feedback_submitters(customer_id)\n",
  },
  {
    "id": "6.3",
    "lesson": 6,
    "difficulty": "easy",
    "title": "Comparing to an Aggregate with a Scalar Subquery",
    "concept": "scalar subquery in WHERE",
    "tables": "orders(order_id, customer_id, amount)",
    "prompt": "Return every `order_id`, `customer_id`, and `amount` where the order's `amount` is strictly greater than the average `amount` across all orders.\n\nOrder by `order_id`.",
    "schemaSql": SCHEMAS.orders3,
    "solutionSql": "select\n    order_id\n  , customer_id\n  , amount\nfrom orders\nwhere amount > (select avg(amount) from orders)\norder by order_id",
    "hint": "`where amount > (select avg(amount) from orders)` -- the subquery returns a single number.",
    "starter": "-- orders(order_id, customer_id, amount)\n",
  },
  {
    "id": "6.4",
    "lesson": 6,
    "difficulty": "easy",
    "title": "Filtering with IN and a Subquery",
    "concept": "IN with subquery",
    "tables": "orders(order_id, customer_id, amount)\ncustomers(customer_id, region)",
    "prompt": "Return every `order_id`, `customer_id`, and `amount` from `orders` where the `customer_id` belongs to a customer in the `'west'` region.\n\nOrder by `order_id`.",
    "schemaSql": SCHEMAS.ordersCustomers,
    "solutionSql": "select\n    order_id\n  , customer_id\n  , amount\nfrom orders\nwhere customer_id in (select customer_id from customers where region = 'west')\norder by order_id",
    "hint": "`where customer_id in (select customer_id from customers where region = 'west')`.",
    "starter": "-- orders(order_id, customer_id, amount)\n  -- customers(customer_id, region)\n",
  },
  {
    "id": "6.5",
    "lesson": 6,
    "difficulty": "easy",
    "title": "Combining a Subquery with a Set Operation",
    "concept": "subquery + EXCEPT",
    "tables": "customers(customer_id, region)\norders(order_id, customer_id, amount)",
    "prompt": "Return the `customer_id`s of customers in the `'west'` region who have never placed an order. Order by `customer_id`.",
    "schemaSql": SCHEMAS.customersOrders2,
    "solutionSql": "select customer_id from customers where region = 'west'\nexcept\nselect customer_id from orders\norder by customer_id",
    "hint": "Filter `customers` down to `region = 'west'` first, then `except` against all `orders.customer_id`.",
    "starter": "-- customers(customer_id, region)\n  -- orders(order_id, customer_id, amount)\n",
  },
  {
    "id": "7.1",
    "lesson": 7,
    "difficulty": "medium",
    "title": "The staging pattern: source -> renamed",
    "concept": "WITH ... AS staging CTEs",
    "tables": "source_subscriptions(sub_id, account_id, plan_code, start_date, end_date, mrr, is_trial)",
    "prompt": "Almost every staging model in this repo follows a `source` CTE -> `renamed` CTE -> final select pattern.\n\nWrite a query with a `source` CTE selecting from `source_subscriptions`, and a `renamed` CTE that renames `sub_id` -> `subscription_id` and `mrr` -> `monthly_recurring_revenue` (keep `account_id` and `plan_code` as-is).\n\nSelect all columns from `renamed`, ordered by `subscription_id`.",
    "schemaSql": SCHEMAS.sourceAccountsSourceSubscriptions,
    "solutionSql": "WITH source AS (\n    SELECT * FROM source_subscriptions\n),\nrenamed AS (\n    SELECT\n        sub_id AS subscription_id\n        , account_id\n        , plan_code\n        , mrr AS monthly_recurring_revenue\n    FROM source\n)\nSELECT * FROM renamed ORDER BY subscription_id;",
    "hint": "WITH source AS (SELECT * FROM source_subscriptions), renamed AS (SELECT sub_id AS subscription_id, account_id, plan_code, mrr AS monthly_recurring_revenue FROM source) SELECT * FROM renamed ...",
    "starter": "-- source_subscriptions(sub_id, account_id, plan_code, start_date, end_date, mrr, is_trial)\n",
  },
  {
    "id": "7.2",
    "lesson": 7,
    "difficulty": "medium",
    "title": "Chaining CTEs across two sources",
    "concept": "Multiple named CTEs joined in the final select",
    "tables": "source_subscriptions(sub_id, account_id, plan_code, ..., is_trial)\nsource_accounts(account_id, account_name, segment)",
    "prompt": "Build a query with two CTEs: `subs` (subscriptions where is_trial = false) and `accounts` (all of source_accounts). Join them in the final select to return `account_name`, `plan_code`, and `mrr` for every non-trial subscription.\n\nOrder by `account_name`, then `plan_code`.",
    "schemaSql": SCHEMAS.sourceAccountsSourceSubscriptions,
    "solutionSql": "WITH subs AS (\n  SELECT * FROM source_subscriptions WHERE is_trial = false\n),\naccounts AS (\n  SELECT * FROM source_accounts\n)\nSELECT a.account_name, s.plan_code, s.mrr\nFROM subs s\nJOIN accounts a ON s.account_id = a.account_id\nORDER BY a.account_name, s.plan_code;",
    "hint": "Define subs and accounts as separate CTEs, then JOIN them ON account_id in the final SELECT.",
    "starter": "-- source_subscriptions(sub_id, account_id, plan_code, start_date, end_date, mrr, is_trial)\n-- source_accounts(account_id, account_name, segment)\n",
  },
  {
    "id": "7.3",
    "lesson": 7,
    "difficulty": "medium",
    "title": "Combining sources with UNION ALL",
    "concept": "UNION ALL + literal tagging column",
    "tables": "source_subscriptions(account_id, plan_code, ...)\nlegacy_subscriptions(account_id, plan_code)",
    "prompt": "There's a small `legacy_subscriptions` table left over from a previous system, with the same account_id/plan_code shape.\n\nReturn `account_id`, `plan_code`, and a literal column `source_system` set to 'current' for rows from `source_subscriptions`, UNION ALL with rows from `legacy_subscriptions` tagged 'legacy'.\n\nOrder by `account_id`, then `source_system`.",
    "schemaSql": SCHEMAS.sourceAccountsSourceSubscriptions,
    "solutionSql": "SELECT account_id, plan_code, 'current' AS source_system FROM source_subscriptions\nUNION ALL\nSELECT account_id, plan_code, 'legacy' AS source_system FROM legacy_subscriptions\nORDER BY account_id, source_system;",
    "hint": "SELECT ... , 'current' AS source_system FROM source_subscriptions UNION ALL SELECT ..., 'legacy' AS source_system FROM legacy_subscriptions",
    "starter": "-- source_subscriptions(sub_id, account_id, plan_code, ...)\n-- legacy_subscriptions(account_id, plan_code)\n",
  },
  {
    "id": "7.4",
    "lesson": 7,
    "difficulty": "medium",
    "title": "Simulating ref()-layered staging models",
    "concept": "stg_ CTEs + LEFT JOIN + COALESCE default",
    "tables": "source_subscriptions(sub_id, account_id, plan_code, mrr, is_trial)\nsource_accounts(account_id, account_name, segment)",
    "prompt": "Models here almost never query raw sources directly -- they build through ref()'d staging models. Simulate that layering:\n\nBuild a `stg_subscriptions` CTE (non-trial subscriptions only) and a `stg_accounts` CTE, then a final `joined` CTE that connects stg_subscriptions to stg_accounts, keeping every subscription even if its account record is missing.\n\nFrom `joined`, select `account_name` (defaulted to 'Unknown' if the account record is missing), `plan_code`, and `mrr`.\n\nOrder by `plan_code`, then `account_name`.\n\n(One subscription in the sample data references an account_id that doesn't exist in source_accounts -- that's the row your default needs to catch.)",
    "schemaSql": SCHEMAS.sourceAccountsSourceSubscriptions,
    "solutionSql": "WITH stg_subscriptions AS (\n  SELECT * FROM source_subscriptions WHERE is_trial = false\n),\nstg_accounts AS (\n  SELECT * FROM source_accounts\n),\njoined AS (\n  SELECT s.plan_code, s.mrr, a.account_name\n  FROM stg_subscriptions s\n  LEFT JOIN stg_accounts a ON s.account_id = a.account_id\n)\nSELECT COALESCE(account_name, 'Unknown') AS account_name, plan_code, mrr\nFROM joined\nORDER BY plan_code, account_name;",
    "hint": "LEFT JOIN inside the joined CTE, then COALESCE(account_name, 'Unknown') in the outer select.",
    "starter": "-- source_subscriptions(sub_id, account_id, plan_code, mrr, is_trial)\n-- source_accounts(account_id, account_name, segment)\n",
  },
  {
    "id": "7.5",
    "lesson": 7,
    "difficulty": "medium",
    "title": "Capstone: staging + CASE tier",
    "concept": "CTEs + JOIN + CASE",
    "tables": "source_subscriptions(sub_id, account_id, plan_code, mrr, is_trial)\nsource_accounts(account_id, account_name, segment)",
    "prompt": "Write a query with `subs` and `accounts` CTEs that returns, for every subscription (trial or not): `account_name`, `plan_code`, `mrr`, and a computed `plan_tier` column ('trial' when is_trial, else 'paid').\n\nOrder by `account_name`, then `plan_code`.",
    "schemaSql": SCHEMAS.sourceAccountsSourceSubscriptions,
    "solutionSql": "WITH subs AS (\n  SELECT * FROM source_subscriptions\n),\naccounts AS (\n  SELECT * FROM source_accounts\n)\nSELECT a.account_name, s.plan_code, s.mrr,\n       CASE WHEN s.is_trial THEN 'trial' ELSE 'paid' END AS plan_tier\nFROM subs s\nJOIN accounts a ON s.account_id = a.account_id\nORDER BY a.account_name, s.plan_code;",
    "hint": "Join the two CTEs, then add CASE WHEN is_trial THEN 'trial' ELSE 'paid' END AS plan_tier.",
    "starter": "-- source_subscriptions(sub_id, account_id, plan_code, mrr, is_trial)\n-- source_accounts(account_id, account_name, segment)\n",
  },
  {
    "id": "8.1",
    "lesson": 8,
    "difficulty": "medium",
    "title": "ROW_NUMBER over a partition",
    "concept": "ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)",
    "tables": "events(event_id, user_id, event_type, event_ts, session_id)",
    "prompt": "For each `user_id` in `events`, number their events in chronological order (1 = earliest) as `event_seq`.\n\nReturn `user_id`, `event_type`, `event_ts`, `event_seq`, ordered by `user_id`, then `event_seq`.",
    "schemaSql": SCHEMAS.eventsSubscriptionHistory,
    "solutionSql": "SELECT user_id, event_type, event_ts, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts) AS event_seq FROM events ORDER BY user_id, event_seq;",
    "hint": "ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts) AS event_seq",
    "starter": "-- events(event_id, user_id, event_type, event_ts, session_id)\n",
  },
  {
    "id": "8.2",
    "lesson": 8,
    "difficulty": "medium",
    "title": "Dedup with QUALIFY",
    "concept": "Snowflake's QUALIFY clause",
    "tables": "events(event_id, user_id, event_type, event_ts, session_id)",
    "prompt": "Snowflake's `QUALIFY` clause lets you filter on a window function result without a wrapping subquery -- this repo uses it constantly to dedupe.\n\nReturn one row per `user_id`: only their most recent event (latest `event_ts`).\n\nReturn `user_id`, `event_type`, `event_ts`, ordered by `user_id`.",
    "schemaSql": SCHEMAS.eventsSubscriptionHistory,
    "solutionSql": "SELECT user_id, event_type, event_ts FROM events QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts DESC) = 1 ORDER BY user_id;",
    "hint": "SELECT ... FROM events QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts DESC) = 1",
    "starter": "-- events(event_id, user_id, event_type, event_ts, session_id)\n",
  },
  {
    "id": "8.3",
    "lesson": 8,
    "difficulty": "medium",
    "title": "LAG for the previous value",
    "concept": "LAG() OVER (PARTITION BY ... ORDER BY ...)",
    "tables": "subscription_history(sub_id, account_id, status, effective_date)",
    "prompt": "`subscription_history` has one row per status change per `sub_id`. Return `sub_id`, `effective_date`, `status`, and the previous status for that `sub_id` (alias `previous_status`, NULL if none).\n\nOrder by `sub_id`, then `effective_date`.",
    "schemaSql": SCHEMAS.eventsSubscriptionHistory,
    "solutionSql": "SELECT sub_id, effective_date, status, LAG(status) OVER (PARTITION BY sub_id ORDER BY effective_date) AS previous_status FROM subscription_history ORDER BY sub_id, effective_date;",
    "hint": "LAG(status) OVER (PARTITION BY sub_id ORDER BY effective_date) AS previous_status",
    "starter": "-- subscription_history(sub_id, account_id, status, effective_date)\n",
  },
  {
    "id": "8.4",
    "lesson": 8,
    "difficulty": "medium",
    "title": "DENSE_RANK within a session",
    "concept": "DENSE_RANK() OVER (PARTITION BY ...)",
    "tables": "events(event_id, user_id, event_type, event_ts, session_id)",
    "prompt": "Rank events within each `session_id` by `event_ts` (earliest = 1), aliased `session_rank`.\n\nReturn `session_id`, `event_id`, `event_ts`, `session_rank`, ordered by `session_id`, then `session_rank`.",
    "schemaSql": SCHEMAS.eventsSubscriptionHistory,
    "solutionSql": "SELECT session_id, event_id, event_ts, DENSE_RANK() OVER (PARTITION BY session_id ORDER BY event_ts) AS session_rank FROM events ORDER BY session_id, session_rank;",
    "hint": "DENSE_RANK() OVER (PARTITION BY session_id ORDER BY event_ts) AS session_rank",
    "starter": "-- events(event_id, user_id, event_type, event_ts, session_id)\n",
  },
  {
    "id": "8.5",
    "lesson": 8,
    "difficulty": "medium",
    "title": "Capstone: detecting status changes",
    "concept": "LAG + CASE + IS DISTINCT FROM",
    "tables": "subscription_history(sub_id, account_id, status, effective_date)",
    "prompt": "Return `sub_id`, `effective_date`, `status`, and a boolean column `status_changed` indicating whether status differs from the previous row's status for that `sub_id`. The first row for a `sub_id` should always show `status_changed = true`.\n\nOrder by `sub_id`, then `effective_date`.",
    "schemaSql": SCHEMAS.eventsSubscriptionHistory,
    "solutionSql": "SELECT sub_id, effective_date, status,\n   CASE WHEN LAG(status) OVER (PARTITION BY sub_id ORDER BY effective_date) IS DISTINCT FROM status THEN true ELSE false END AS status_changed\nFROM subscription_history\nORDER BY sub_id, effective_date;",
    "hint": "CASE WHEN LAG(status) OVER (PARTITION BY sub_id ORDER BY effective_date) IS DISTINCT FROM status THEN true ELSE false END",
    "starter": "-- subscription_history(sub_id, account_id, status, effective_date)\n",
  },
  {
    "id": "9.1",
    "lesson": 9,
    "difficulty": "medium",
    "title": "Simulating a not_null test",
    "concept": "What dbt's not_null generic test runs under the hood",
    "tables": "accounts(account_id, account_name, owner_id, region, created_at)",
    "prompt": "dbt's `not_null` generic test works by finding rows where the column IS NULL -- if any come back, the test fails.\n\nWrite the query dbt would effectively run to test that `owner_id` is not_null on `accounts` -- return all columns for the rows that would fail this test.",
    "schemaSql": SCHEMAS.accountsPlanAccounts,
    "solutionSql": "SELECT * FROM accounts WHERE owner_id IS NULL;",
    "hint": "SELECT * FROM accounts WHERE owner_id IS NULL",
    "starter": "-- accounts(account_id, account_name, owner_id, region, created_at)\n",
  },
  {
    "id": "9.2",
    "lesson": 9,
    "difficulty": "medium",
    "title": "Simulating a unique test",
    "concept": "What dbt's unique generic test runs under the hood",
    "tables": "accounts(account_id, account_name, owner_id, region, created_at)",
    "prompt": "dbt's unique test finds duplicate values. Write a query that returns `account_id` and the count of times it appears in `accounts` (as `n`), but only for account_ids appearing more than once -- the rows a unique test would flag.\n\nOrder by `account_id`.",
    "schemaSql": SCHEMAS.accountsPlanAccounts,
    "solutionSql": "SELECT account_id, COUNT(*) AS n FROM accounts GROUP BY account_id HAVING COUNT(*) > 1 ORDER BY account_id;",
    "hint": "GROUP BY account_id HAVING COUNT(*) > 1",
    "starter": "-- accounts(account_id, account_name, owner_id, region, created_at)\n",
  },
  {
    "id": "9.3",
    "lesson": 9,
    "difficulty": "medium",
    "title": "Simulating a relationships test",
    "concept": "What dbt's relationships generic test runs under the hood",
    "tables": "plan_accounts(plan_id, account_id)\naccounts(account_id, account_name, ...)",
    "prompt": "dbt's relationships test checks that every child key exists in its parent table.\n\nWrite a query that returns `plan_id` and `account_id` from `plan_accounts` for rows whose account_id does not exist in `accounts` -- orphaned foreign keys a failing relationships test would surface.\n\nOrder by `plan_id`.",
    "schemaSql": SCHEMAS.accountsPlanAccounts,
    "solutionSql": "SELECT p.plan_id, p.account_id FROM plan_accounts p LEFT JOIN accounts a ON p.account_id = a.account_id WHERE a.account_id IS NULL ORDER BY p.plan_id;",
    "hint": "LEFT JOIN plan_accounts to accounts, then WHERE a.account_id IS NULL to find the orphans.",
    "starter": "-- plan_accounts(plan_id, account_id)\n-- accounts(account_id, account_name, ...)\n",
  },
  {
    "id": "9.4",
    "lesson": 9,
    "difficulty": "medium",
    "title": "Date arithmetic",
    "concept": "INTERVAL arithmetic (DATEADD equivalent)",
    "tables": "accounts(account_id, account_name, owner_id, region, created_at)",
    "prompt": "This repo's Snowflake SQL often needs to add a fixed number of days to a date. Return `account_id`, `account_name`, `created_at`, and a column `stale_after` representing the date 90 days after `created_at`.\n\nOrder by `account_id`.",
    "schemaSql": SCHEMAS.accountsPlanAccounts,
    "solutionSql": "SELECT account_id, account_name, created_at, created_at + INTERVAL 90 DAY AS stale_after FROM accounts ORDER BY account_id;",
    "hint": "created_at + INTERVAL 90 DAY AS stale_after",
    "starter": "-- accounts(account_id, account_name, owner_id, region, created_at)\n",
  },
  {
    "id": "9.5",
    "lesson": 9,
    "difficulty": "medium",
    "title": "Capstone: simulating an is_incremental() filter",
    "concept": "Date filtering, as if branching on is_incremental()",
    "tables": "accounts(account_id, account_name, owner_id, region, created_at)",
    "prompt": "dbt models often branch logic with {% if is_incremental() %}, usually to add a recency filter. Simulate that filter here.\n\nPretend \"today\" is DATE '2024-04-01' (don't use CURRENT_DATE for this exercise -- hardcode that literal). Return `account_id`, `account_name`, `created_at` for accounts created within the last 60 days of that date.\n\nOrder by `created_at`.",
    "schemaSql": SCHEMAS.accountsPlanAccounts,
    "solutionSql": "SELECT account_id, account_name, created_at FROM accounts WHERE created_at >= DATE '2024-04-01' - INTERVAL 60 DAY ORDER BY created_at;",
    "hint": "WHERE created_at >= DATE '2024-04-01' - INTERVAL 60 DAY",
    "starter": "-- accounts(account_id, account_name, owner_id, region, created_at)\n",
  },
  {
    "id": "10.1",
    "lesson": 10,
    "difficulty": "medium",
    "title": "Running Totals with SUM() OVER",
    "concept": "SUM() OVER (running total)",
    "tables": "payments(payment_id, account_id, paid_at, amount)",
    "prompt": "For each `account_id`, return `payment_id`, `paid_at`, `amount`, and a `running_total` that sums `amount` for that account so far, ordered by `paid_at`. Order by `account_id`, `paid_at`.",
    "schemaSql": SCHEMAS.payments,
    "solutionSql": "select\n    payment_id\n  , account_id\n  , paid_at\n  , amount\n  , sum(amount) over (partition by account_id order by paid_at) as running_total\nfrom payments\norder by account_id, paid_at",
    "hint": "`sum(amount) over (partition by account_id order by paid_at)` -- the default frame accumulates rows so far.",
    "starter": "-- payments(payment_id, account_id, paid_at, amount)\n",
  },
  {
    "id": "10.2",
    "lesson": 10,
    "difficulty": "medium",
    "title": "Moving Averages with a ROWS Frame",
    "concept": "AVG() OVER (ROWS BETWEEN)",
    "tables": "daily_signups(signup_date, signup_count)",
    "prompt": "Return `signup_date`, `signup_count`, and a 3-day moving average `moving_avg` (the current row plus the 2 preceding rows, ordered by `signup_date`). Order by `signup_date`.",
    "schemaSql": SCHEMAS.dailySignups,
    "solutionSql": "select\n    signup_date\n  , signup_count\n  , avg(signup_count) over (\n      order by signup_date\n      rows between 2 preceding and current row\n    ) as moving_avg\nfrom daily_signups\norder by signup_date",
    "hint": "`avg(signup_count) over (order by signup_date rows between 2 preceding and current row)`.",
    "starter": "-- daily_signups(signup_date, signup_count)\n",
  },
  {
    "id": "10.3",
    "lesson": 10,
    "difficulty": "medium",
    "title": "Bucketing Rows with NTILE",
    "concept": "NTILE",
    "tables": "customers(customer_id, lifetime_value)",
    "prompt": "Return `customer_id`, `lifetime_value`, and a `value_quartile` from 1 to 4 assigning each customer to a quartile by `lifetime_value` descending (quartile 1 = highest value). Order by `customer_id`.",
    "schemaSql": SCHEMAS.customers2,
    "solutionSql": "select\n    customer_id\n  , lifetime_value\n  , ntile(4) over (order by lifetime_value desc) as value_quartile\nfrom customers\norder by customer_id",
    "hint": "`ntile(4) over (order by lifetime_value desc)` splits the ordered rows into 4 roughly equal buckets.",
    "starter": "-- customers(customer_id, lifetime_value)\n",
  },
  {
    "id": "10.4",
    "lesson": 10,
    "difficulty": "medium",
    "title": "Grabbing Endpoints with FIRST_VALUE/LAST_VALUE",
    "concept": "FIRST_VALUE/LAST_VALUE",
    "tables": "orders(order_id, customer_id, order_date, amount)",
    "prompt": "For each `customer_id`, return every `order_id`, `order_date`, `amount`, the customer's `first_order_amount` (the `amount` of their earliest order), and `last_order_amount` (the `amount` of their latest order). Order by `customer_id`, `order_date`.",
    "schemaSql": SCHEMAS.orders4,
    "solutionSql": "select\n    order_id\n  , customer_id\n  , order_date\n  , amount\n  , first_value(amount) over (\n      partition by customer_id order by order_date\n    ) as first_order_amount\n  , last_value(amount) over (\n      partition by customer_id order by order_date\n      rows between unbounded preceding and unbounded following\n    ) as last_order_amount\nfrom orders\norder by customer_id, order_date",
    "hint": "`first_value` works with the default frame, but `last_value` needs `rows between unbounded preceding and unbounded following` to see the whole partition.",
    "starter": "-- orders(order_id, customer_id, order_date, amount)\n",
  },
  {
    "id": "10.5",
    "lesson": 10,
    "difficulty": "medium",
    "title": "Capstone: Running Totals with Value Tiers",
    "concept": "running total + NTILE",
    "tables": "payments(payment_id, account_id, paid_at, amount)",
    "prompt": "Return `payment_id`, `account_id`, `paid_at`, `amount`, a `running_total` per `account_id` ordered by `paid_at`, and a `payment_tier` from 1 to 2 splitting ALL payments (not partitioned) into 2 buckets ordered by `amount` descending. Order by `account_id`, `paid_at`.",
    "schemaSql": SCHEMAS.payments1,
    "solutionSql": "select\n    payment_id\n  , account_id\n  , paid_at\n  , amount\n  , sum(amount) over (partition by account_id order by paid_at) as running_total\n  , ntile(2) over (order by amount desc) as payment_tier\nfrom payments\norder by account_id, paid_at",
    "hint": "Combine two window functions in the same select: one `partition by account_id` for the running total, one unpartitioned `ntile(2)` for the tier.",
    "starter": "-- payments(payment_id, account_id, paid_at, amount)\n",
  },
  {
    "id": "11.1",
    "lesson": 11,
    "difficulty": "medium",
    "title": "Self-Join for Manager Names",
    "concept": "self-join",
    "tables": "employees(employee_id, employee_name, manager_id)",
    "prompt": "`employees.manager_id` refers back to another row's `employee_id`. Join `employees` to itself to return each `employee_id`, `employee_name`, and their `manager_name` (null if they have no manager -- such employees should still appear in the result).\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.employees1,
    "solutionSql": "select\n    e.employee_id\n  , e.employee_name\n  , m.employee_name as manager_name\nfrom employees as e\nleft join employees as m\n  on e.manager_id = m.employee_id\norder by e.employee_id",
    "hint": "Alias the table twice, e.g. `employees as e` and `employees as m`, joining `e.manager_id = m.employee_id`.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n",
  },
  {
    "id": "11.2",
    "lesson": 11,
    "difficulty": "medium",
    "title": "Keeping Both Sides with FULL OUTER JOIN",
    "concept": "FULL OUTER JOIN",
    "tables": "product_catalog(product_id, product_name)\ninventory(product_id, quantity_on_hand)",
    "prompt": "Return every `product_id` (from either table), `product_name`, and `quantity_on_hand` for the full picture of catalog vs. inventory records -- including catalog products missing inventory rows and inventory rows for products no longer in the catalog. Combine the `product_id` from both sides into one column.\n\nOrder by `product_id`.",
    "schemaSql": SCHEMAS.productCatalogInventory,
    "solutionSql": "select\n    coalesce(c.product_id, i.product_id) as product_id\n  , c.product_name\n  , i.quantity_on_hand\nfrom product_catalog as c\nfull outer join inventory as i\n  on c.product_id = i.product_id\norder by product_id",
    "hint": "`full outer join` keeps unmatched rows from both sides; `coalesce(c.product_id, i.product_id)` picks whichever side has a value.",
    "starter": "-- product_catalog(product_id, product_name)\n  -- inventory(product_id, quantity_on_hand)\n",
  },
  {
    "id": "11.3",
    "lesson": 11,
    "difficulty": "medium",
    "title": "Joining on Multiple Conditions",
    "concept": "multi-condition ON clause",
    "tables": "shipments(shipment_id, warehouse_code, order_id, shipped_at)\nwarehouse_rates(warehouse_code, effective_year, rate_per_unit)",
    "prompt": "`warehouse_rates` has a different `rate_per_unit` per `warehouse_code` per `effective_year`. Join `shipments` to `warehouse_rates` matching BOTH `warehouse_code` and the shipment's shipped year to `effective_year`. Return `shipment_id`, `warehouse_code`, `shipped_at`, and `rate_per_unit`. Order by `shipment_id`.",
    "schemaSql": SCHEMAS.shipmentsWarehouseRates,
    "solutionSql": "select\n    s.shipment_id\n  , s.warehouse_code\n  , s.shipped_at\n  , r.rate_per_unit\nfrom shipments as s\ninner join warehouse_rates as r\n  on s.warehouse_code = r.warehouse_code\n and extract(year from s.shipped_at) = r.effective_year\norder by s.shipment_id",
    "hint": "The `on` clause needs two conditions joined with `and`: matching `warehouse_code` AND matching year to `effective_year`.",
    "starter": "-- shipments(shipment_id, warehouse_code, order_id, shipped_at)\n  -- warehouse_rates(warehouse_code, effective_year, rate_per_unit)\n",
  },
  {
    "id": "11.4",
    "lesson": 11,
    "difficulty": "medium",
    "title": "Finding Peers via Self-Join",
    "concept": "self-join with filter",
    "tables": "employees(employee_id, employee_name, department, manager_id)",
    "prompt": "Return pairs of DIFFERENT employees who share the same manager (peers on the same team), as `employee_a` and `employee_b`. Make sure each pair appears only once \u2014 not reversed, and not paired with themselves.\n\nOrder by `employee_a`, `employee_b`.",
    "schemaSql": SCHEMAS.employees2,
    "solutionSql": "select\n    e1.employee_name as employee_a\n  , e2.employee_name as employee_b\nfrom employees as e1\ninner join employees as e2\n  on e1.manager_id = e2.manager_id\n and e1.employee_id < e2.employee_id\norder by employee_a, employee_b",
    "hint": "The `e1.employee_id < e2.employee_id` condition both excludes self-pairs and prevents each pair from showing up twice.",
    "starter": "-- employees(employee_id, employee_name, department, manager_id)\n",
  },
  {
    "id": "11.5",
    "lesson": 11,
    "difficulty": "medium",
    "title": "Capstone: Full Roster Reconciliation",
    "concept": "self-join + FULL OUTER JOIN",
    "tables": "employees(employee_id, employee_name, manager_id)\npayroll_records(employee_id, salary)",
    "prompt": "Reconcile `employees` against `payroll_records` so that no row from either side is lost, even when there's no match on the other side (some employees have no payroll record yet; some payroll records reference ex-employees no longer in `employees`). Then look up each employee's `manager_name` from `employees` itself. Return a unified `employee_id`, `e.employee_name`, `manager_name`, and `p.salary`. Order by `employee_id`.",
    "schemaSql": SCHEMAS.employeesPayrollRecords,
    "solutionSql": "select\n    coalesce(e.employee_id, p.employee_id) as employee_id\n  , e.employee_name\n  , m.employee_name as manager_name\n  , p.salary\nfrom employees as e\nfull outer join payroll_records as p\n  on e.employee_id = p.employee_id\nleft join employees as m\n  on e.manager_id = m.employee_id\norder by employee_id",
    "hint": "First `full outer join` employees to payroll_records and coalesce the id; then a separate `left join` back to `employees` (aliased differently) for the manager name.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n  -- payroll_records(employee_id, salary)\n",
  },
  {
    "id": "12.1",
    "lesson": 12,
    "difficulty": "medium",
    "title": "Simulating an accepted_values Test",
    "concept": "accepted_values simulation",
    "tables": "subscriptions(subscription_id, status)",
    "prompt": "dbt's `accepted_values` generic test would flag any `status` outside `('active', 'trialing', 'cancelled', 'past_due')`. Simulate that test yourself: return the `subscription_id` and `status` of every row that would fail the test. Order by `subscription_id`.",
    "schemaSql": SCHEMAS.subscriptions2,
    "solutionSql": "select\n    subscription_id\n  , status\nfrom subscriptions\nwhere status not in ('active', 'trialing', 'cancelled', 'past_due')\norder by subscription_id",
    "hint": "A passing `accepted_values` test has zero rows returned by `where status not in (...)` -- return the failures.",
    "starter": "-- subscriptions(subscription_id, status)\n",
  },
  {
    "id": "12.2",
    "lesson": 12,
    "difficulty": "medium",
    "title": "Uniqueness Across a Column Combination",
    "concept": "composite uniqueness test",
    "tables": "price_history(product_id, effective_date, price)",
    "prompt": "dbt's `dbt_utils.unique_combination_of_columns` test would check that `(product_id, effective_date)` is unique in `price_history`. Simulate that: return the `product_id`, `effective_date`, and `row_count` for any combination appearing more than once -- these are the rows that would fail the test.\n\nOrder by `product_id`, `effective_date`.",
    "schemaSql": SCHEMAS.priceHistory,
    "solutionSql": "select\n    product_id\n  , effective_date\n  , count(*) as row_count\nfrom price_history\ngroup by product_id, effective_date\nhaving count(*) > 1\norder by product_id, effective_date",
    "hint": "`group by product_id, effective_date` then `having count(*) > 1` surfaces the duplicated combinations.",
    "starter": "-- price_history(product_id, effective_date, price)\n",
  },
  {
    "id": "12.3",
    "lesson": 12,
    "difficulty": "medium",
    "title": "Joining a Static Lookup (Seed) Table",
    "concept": "static lookup table join",
    "tables": "orders(order_id, status_code, amount)\nstatus_lookup(status_code, status_label)",
    "prompt": "`status_lookup` is a small seed-style reference table (like a dbt seed csv) mapping raw `status_code`s to friendly labels. Join `orders` to `status_lookup` to return `order_id`, `amount`, and the human-readable `status_label`. Order by `order_id`.",
    "schemaSql": SCHEMAS.ordersStatusLookup,
    "solutionSql": "select\n    o.order_id\n  , o.amount\n  , l.status_label\nfrom orders as o\ninner join status_lookup as l\n  on o.status_code = l.status_code\norder by o.order_id",
    "hint": "A plain `inner join` on `status_code` -- treat `status_lookup` exactly like a dbt seed you'd `ref()`.",
    "starter": "-- orders(order_id, status_code, amount)\n  -- status_lookup(status_code, status_label)\n",
  },
  {
    "id": "12.4",
    "lesson": 12,
    "difficulty": "medium",
    "title": "Simulating not_null and relationships Tests",
    "concept": "not_null + relationships simulation",
    "tables": "orders(order_id, customer_id)\ncustomers(customer_id)",
    "prompt": "Simulate two dbt generic tests at once: `not_null` on `orders.customer_id`, and `relationships` (every `orders.customer_id` must exist in `customers.customer_id`). Return the `order_id` of every row that would fail either check. Order by `order_id`.",
    "schemaSql": SCHEMAS.ordersCustomers1,
    "solutionSql": "select\n    order_id\nfrom orders\nwhere customer_id is null\n   or customer_id not in (select customer_id from customers)\norder by order_id",
    "hint": "Combine `customer_id is null` with `or customer_id not in (select customer_id from customers)`.",
    "starter": "-- orders(order_id, customer_id)\n  -- customers(customer_id)\n",
  },
  {
    "id": "12.5",
    "lesson": 12,
    "difficulty": "medium",
    "title": "Capstone: Lookup Join Plus Accepted Values Check",
    "concept": "lookup join + accepted_values",
    "tables": "orders(order_id, status_code, amount)\nstatus_lookup(status_code, status_label, is_valid_status)",
    "prompt": "`status_lookup` now has an `is_valid_status` flag marking which codes are still allowed. Left join `orders` to `status_lookup` on `status_code`, and return `order_id`, `amount`, `status_label`, and a boolean `fails_accepted_values` that is true when there's no matching lookup row at all, OR when `is_valid_status` is false. Order by `order_id`.",
    "schemaSql": SCHEMAS.ordersStatusLookup1,
    "solutionSql": "select\n    o.order_id\n  , o.amount\n  , l.status_label\n  , l.status_code is null or not coalesce(l.is_valid_status, false) as fails_accepted_values\nfrom orders as o\nleft join status_lookup as l\n  on o.status_code = l.status_code\norder by o.order_id",
    "hint": "After a `left join`, an unmatched row has `l.status_code is null`; combine that with `not coalesce(l.is_valid_status, false)`.",
    "starter": "-- orders(order_id, status_code, amount)\n  -- status_lookup(status_code, status_label, is_valid_status)\n",
  },
  {
    "id": "13.1",
    "lesson": 13,
    "difficulty": "hard",
    "title": "The full-refresh query",
    "concept": "incremental model config, baseline",
    "tables": "raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)",
    "prompt": "An incremental model's first (full-refresh) run just selects everything. Write the baseline query: select all columns from `raw_usage_events`, ordered by `event_id`.",
    "schemaSql": SCHEMAS.existingTargetRawUsageEvents,
    "solutionSql": "SELECT event_id, account_id, event_type, event_date, loaded_at FROM raw_usage_events ORDER BY event_id;",
    "hint": "A plain SELECT * (or explicit column list) FROM raw_usage_events ORDER BY event_id.",
    "starter": "-- raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)\n",
  },
  {
    "id": "13.2",
    "lesson": 13,
    "difficulty": "hard",
    "title": "The is_incremental() filter",
    "concept": "{% if is_incremental() %} WHERE loaded_at > max(...)",
    "tables": "raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)\nexisting_target(same shape, already materialized)",
    "prompt": "On subsequent incremental runs, dbt's `{% if is_incremental() %}` block typically adds a filter so only new rows get processed.\n\n`existing_target` represents what's already in the warehouse. Write that filtered query against `raw_usage_events`: only rows that are newer than what's already been loaded into `existing_target`.\n\nReturn the same columns as 13.1, ordered by `event_id`.",
    "schemaSql": SCHEMAS.existingTargetRawUsageEvents,
    "solutionSql": "SELECT event_id, account_id, event_type, event_date, loaded_at FROM raw_usage_events WHERE loaded_at > (SELECT MAX(loaded_at) FROM existing_target) ORDER BY event_id;",
    "hint": "WHERE loaded_at > (SELECT MAX(loaded_at) FROM existing_target)",
    "starter": "-- raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)\n-- existing_target(event_id, account_id, event_type, event_date, loaded_at)\n",
  },
  {
    "id": "13.3",
    "lesson": 13,
    "difficulty": "hard",
    "title": "Simulating a merge on unique_key",
    "concept": "incremental_strategy = 'merge'",
    "tables": "existing_target + raw_usage_events, both same shape",
    "prompt": "A model configured with `unique_key='event_id'` and `incremental_strategy='merge'`: when an incoming `event_id` already exists in the target, the incoming row replaces it.\n\nSimulate the merge result: combine `existing_target` and `raw_usage_events`, then keep just one row per `event_id` -- the version with the greatest `loaded_at`.\n\nReturn `event_id`, `account_id`, `event_type`, `event_date`, `loaded_at`, ordered by `event_id`.",
    "schemaSql": SCHEMAS.existingTargetRawUsageEvents,
    "solutionSql": "WITH combined AS (\n  SELECT * FROM existing_target\n  UNION ALL\n  SELECT * FROM raw_usage_events\n)\nSELECT event_id, account_id, event_type, event_date, loaded_at\nFROM combined\nQUALIFY ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY loaded_at DESC) = 1\nORDER BY event_id;",
    "hint": "UNION ALL the two tables in a CTE, then QUALIFY ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY loaded_at DESC) = 1.",
    "starter": "-- existing_target(event_id, account_id, event_type, event_date, loaded_at)\n-- raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)\n",
  },
  {
    "id": "13.4",
    "lesson": 13,
    "difficulty": "hard",
    "title": "Simulating delete+insert: latest state per key",
    "concept": "incremental_strategy = 'delete+insert', latest-row-per-key",
    "tables": "raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)",
    "prompt": "delete+insert incremental models often keep just the latest known state per key. Return only the most recent event per `account_id` from `raw_usage_events` (the row with the latest `event_date`, tie-broken by the latest `loaded_at`).\n\nReturn `account_id`, `event_type`, `event_date`, `loaded_at`, ordered by `account_id`.",
    "schemaSql": SCHEMAS.existingTargetRawUsageEvents,
    "solutionSql": "SELECT account_id, event_type, event_date, loaded_at FROM raw_usage_events QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY event_date DESC, loaded_at DESC) = 1 ORDER BY account_id;",
    "hint": "QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY event_date DESC, loaded_at DESC) = 1",
    "starter": "-- raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)\n",
  },
  {
    "id": "13.5",
    "lesson": 13,
    "difficulty": "hard",
    "title": "Capstone: incremental filter + latest-per-key",
    "concept": "Combining is_incremental() filtering with dedup",
    "tables": "raw_usage_events + existing_target",
    "prompt": "Combine both concepts: from `raw_usage_events`, keep only rows newer than existing_target's max loaded_at (the incremental filter from 13.2), and within that filtered set return just the latest event per account_id (as in 13.4).\n\nReturn `account_id`, `event_type`, `event_date`, `loaded_at`, ordered by `account_id`.",
    "schemaSql": SCHEMAS.existingTargetRawUsageEvents,
    "solutionSql": "WITH new_rows AS (\n  SELECT * FROM raw_usage_events WHERE loaded_at > (SELECT MAX(loaded_at) FROM existing_target)\n)\nSELECT account_id, event_type, event_date, loaded_at\nFROM new_rows\nQUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY event_date DESC, loaded_at DESC) = 1\nORDER BY account_id;",
    "hint": "A new_rows CTE applying the incremental filter, then QUALIFY on top to keep the latest row per account_id.",
    "starter": "-- raw_usage_events(event_id, account_id, event_type, event_date, loaded_at)\n-- existing_target(event_id, account_id, event_type, event_date, loaded_at)\n",
  },
  {
    "id": "14.1",
    "lesson": 14,
    "difficulty": "hard",
    "title": "Extracting a top-level JSON field",
    "concept": "Snowflake VARIANT ':' path access, analog: JSON '->>'",
    "tables": "raw_payloads(id, account_id, payload) -- payload is a JSON string, like a Snowflake VARIANT column",
    "prompt": "`raw_payloads.payload` is a JSON string -- the sandbox's analog to a Snowflake VARIANT column (which you'd normally access with `payload:plan::string`).\n\nReturn `id`, `account_id`, and the extracted `plan` value from the payload.\n\nOrder by `id`.",
    "schemaSql": SCHEMAS.rawPayloads,
    "solutionSql": "SELECT id, account_id, payload::JSON->>'plan' AS plan FROM raw_payloads ORDER BY id;",
    "hint": "payload::JSON->>'plan' AS plan",
    "starter": "-- raw_payloads(id, account_id, payload)\n-- payload example: {\"plan\":\"enterprise\",\"teams\":[{\"team_id\":10,\"seats\":5}],\"features\":[\"sso\"]}\n",
  },
  {
    "id": "14.2",
    "lesson": 14,
    "difficulty": "hard",
    "title": "Flattening a JSON array (LATERAL FLATTEN analog)",
    "concept": "UNNEST as the DuckDB analog to LATERAL FLATTEN",
    "tables": "raw_payloads(id, account_id, payload)",
    "prompt": "Snowflake explodes a JSON array into one row per element with `LATERAL FLATTEN(input => payload:teams)`. DuckDB's equivalent involves casting the array to a typed list and using `UNNEST`.\n\nReturn `id`, `account_id`, `team_id`, and `seats` -- one row per team across all accounts. Accounts with no teams should be skipped automatically.\n\nOrder by `id`, then `team_id`.",
    "schemaSql": SCHEMAS.rawPayloads,
    "solutionSql": "WITH exploded AS (\n  SELECT id, account_id, payload,\n         unnest(CAST(payload::JSON->'teams' AS STRUCT(team_id INTEGER, seats INTEGER)[])) AS team\n  FROM raw_payloads\n)\nSELECT id, account_id, team.team_id, team.seats\nFROM exploded\nORDER BY id, team.team_id;",
    "hint": "Put the unnest(...) AS team expression in a CTE's select list, then reference team.team_id / team.seats in the outer query.",
    "starter": "-- raw_payloads(id, account_id, payload)\n",
  },
  {
    "id": "14.3",
    "lesson": 14,
    "difficulty": "hard",
    "title": "Array length",
    "concept": "len() on a cast JSON array",
    "tables": "raw_payloads(id, account_id, payload)",
    "prompt": "Return `id`, `account_id`, and the number of elements in the `features` array, aliased `feature_count`.\n\nOrder by `id`.",
    "schemaSql": SCHEMAS.rawPayloads,
    "solutionSql": "SELECT id, account_id, len(CAST(payload::JSON->'features' AS VARCHAR[])) AS feature_count FROM raw_payloads ORDER BY id;",
    "hint": "len(CAST(payload::JSON->'features' AS VARCHAR[])) AS feature_count",
    "starter": "-- raw_payloads(id, account_id, payload)\n",
  },
  {
    "id": "14.4",
    "lesson": 14,
    "difficulty": "hard",
    "title": "Filtering on array containment",
    "concept": "list_contains()",
    "tables": "raw_payloads(id, account_id, payload)",
    "prompt": "Return `id`, `account_id` for accounts whose `features` array contains `'sso'`.\n\nOrder by `id`.",
    "schemaSql": SCHEMAS.rawPayloads,
    "solutionSql": "SELECT id, account_id FROM raw_payloads WHERE list_contains(CAST(payload::JSON->'features' AS VARCHAR[]), 'sso') ORDER BY id;",
    "hint": "WHERE list_contains(CAST(payload::JSON->'features' AS VARCHAR[]), 'sso')",
    "starter": "-- raw_payloads(id, account_id, payload)\n",
  },
  {
    "id": "14.5",
    "lesson": 14,
    "difficulty": "hard",
    "title": "Capstone: flatten + top-level field + CASE",
    "concept": "Combining JSON extraction, array flattening, and CASE",
    "tables": "raw_payloads(id, account_id, payload)",
    "prompt": "For every team across all accounts (flatten teams as in 14.2), return `account_id`, the account's `plan` (top-level field), `team_id`, `seats`, and a computed `team_size_tier` column ('large' when seats >= 5, else 'small').\n\nOrder by `account_id`, then `team_id`.",
    "schemaSql": SCHEMAS.rawPayloads,
    "solutionSql": "WITH exploded AS (\n  SELECT id, account_id, payload,\n         unnest(CAST(payload::JSON->'teams' AS STRUCT(team_id INTEGER, seats INTEGER)[])) AS team\n  FROM raw_payloads\n)\nSELECT account_id, payload::JSON->>'plan' AS plan, team.team_id, team.seats,\n       CASE WHEN team.seats >= 5 THEN 'large' ELSE 'small' END AS team_size_tier\nFROM exploded\nORDER BY account_id, team.team_id;",
    "hint": "Reuse the exploded CTE from 14.2, add payload::JSON->>'plan', and a CASE on team.seats.",
    "starter": "-- raw_payloads(id, account_id, payload)\n",
  },
  {
    "id": "15.1",
    "lesson": 15,
    "difficulty": "hard",
    "title": "Hand-rolled surrogate key",
    "concept": "md5(concat(coalesce(...))) -- the mechanics behind dbt_utils.generate_surrogate_key",
    "tables": "daily_feed_day1(employee_id, department, salary)",
    "prompt": "This repo generates surrogate keys via {{ dbt_utils.generate_surrogate_key([...]) }}, which under the hood MD5-hashes the concatenated, null-safe-coalesced columns.\n\nUsing md5(), write a query returning `employee_id`, `department`, and a `surrogate_key` column computed as:\nmd5(coalesce(employee_id::varchar,'') || '-' || coalesce(department,''))\nagainst `daily_feed_day1`.\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.dailyFeedDay1DailyFeedDay2,
    "solutionSql": "SELECT employee_id, department, md5(COALESCE(employee_id::VARCHAR,'') || '-' || COALESCE(department,'')) AS surrogate_key FROM daily_feed_day1 ORDER BY employee_id;",
    "hint": "md5(COALESCE(employee_id::VARCHAR,'') || '-' || COALESCE(department,'')) AS surrogate_key",
    "starter": "-- daily_feed_day1(employee_id, department, salary)\n",
  },
  {
    "id": "15.2",
    "lesson": 15,
    "difficulty": "hard",
    "title": "Snapshot \"check\" strategy: changed rows",
    "concept": "strategy='check' -- detecting column changes between two loads",
    "tables": "daily_feed_day1(yesterday), daily_feed_day2(today) -- same shape",
    "prompt": "A dbt snapshot with `strategy='check'` detects when tracked columns change between runs.\n\nCompare `daily_feed_day1` (yesterday) to `daily_feed_day2` (today) and return `employee_id`, `department`, `salary` from today's feed for every employee whose department or salary changed between the two days -- including a change from/to a missing (null) value.\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.dailyFeedDay1DailyFeedDay2,
    "solutionSql": "SELECT d2.employee_id, d2.department, d2.salary\nFROM daily_feed_day2 d2\nJOIN daily_feed_day1 d1 ON d1.employee_id = d2.employee_id\nWHERE d1.department IS DISTINCT FROM d2.department OR d1.salary IS DISTINCT FROM d2.salary\nORDER BY d2.employee_id;",
    "hint": "JOIN day2 to day1 on employee_id, WHERE d1.department IS DISTINCT FROM d2.department OR d1.salary IS DISTINCT FROM d2.salary.",
    "starter": "-- daily_feed_day1(employee_id, department, salary)\n-- daily_feed_day2(employee_id, department, salary)\n",
  },
  {
    "id": "15.3",
    "lesson": 15,
    "difficulty": "hard",
    "title": "Snapshot: detecting new rows",
    "concept": "Rows a snapshot would insert as brand new",
    "tables": "daily_feed_day1, daily_feed_day2",
    "prompt": "Return the `employee_id` and `department` for employees present in today's feed (daily_feed_day2) but absent from yesterday's (daily_feed_day1) -- the new rows a snapshot would insert.\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.dailyFeedDay1DailyFeedDay2,
    "solutionSql": "SELECT d2.employee_id, d2.department FROM daily_feed_day2 d2 LEFT JOIN daily_feed_day1 d1 ON d1.employee_id = d2.employee_id WHERE d1.employee_id IS NULL ORDER BY d2.employee_id;",
    "hint": "LEFT JOIN day2 to day1, WHERE d1.employee_id IS NULL.",
    "starter": "-- daily_feed_day1(employee_id, department, salary)\n-- daily_feed_day2(employee_id, department, salary)\n",
  },
  {
    "id": "15.4",
    "lesson": 15,
    "difficulty": "hard",
    "title": "Snapshot: invalidate_hard_deletes",
    "concept": "Rows a snapshot would mark as deleted",
    "tables": "daily_feed_day1, daily_feed_day2",
    "prompt": "Return `employee_id` for employees present yesterday but missing from today's feed entirely -- rows a snapshot's invalidate_hard_deletes=true would mark as deleted.\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.dailyFeedDay1DailyFeedDay2,
    "solutionSql": "SELECT d1.employee_id FROM daily_feed_day1 d1 LEFT JOIN daily_feed_day2 d2 ON d1.employee_id = d2.employee_id WHERE d2.employee_id IS NULL ORDER BY d1.employee_id;",
    "hint": "LEFT JOIN day1 to day2, WHERE d2.employee_id IS NULL.",
    "starter": "-- daily_feed_day1(employee_id, department, salary)\n-- daily_feed_day2(employee_id, department, salary)\n",
  },
  {
    "id": "15.5",
    "lesson": 15,
    "difficulty": "hard",
    "title": "Capstone: building valid_from / valid_to",
    "concept": "LEAD() to construct SCD2-style validity windows",
    "tables": "employee_history(employee_id, department, salary, valid_from)",
    "prompt": "`employee_history` has one row per (employee_id, change), each with a valid_from date -- this is what a chain of snapshot runs accumulates over time.\n\nCompute `valid_to` for each row as the next change's `valid_from` for that `employee_id` (leave it NULL for the most recent, still-open row).\n\nReturn `employee_id`, `department`, `salary`, `valid_from`, `valid_to`, ordered by `employee_id`, then `valid_from`.",
    "schemaSql": SCHEMAS.dailyFeedDay1DailyFeedDay2,
    "solutionSql": "SELECT employee_id, department, salary, valid_from, LEAD(valid_from) OVER (PARTITION BY employee_id ORDER BY valid_from) AS valid_to FROM employee_history ORDER BY employee_id, valid_from;",
    "hint": "LEAD(valid_from) OVER (PARTITION BY employee_id ORDER BY valid_from) AS valid_to",
    "starter": "-- employee_history(employee_id, department, salary, valid_from)\n",
  },
  {
    "id": "16.1",
    "lesson": 16,
    "difficulty": "hard",
    "title": "Hand-expanding a type-aware casting macro",
    "concept": "What a Jinja for-loop over columns would generate",
    "tables": "source_a(id, name, amount, created_at)",
    "prompt": "This repo's staging_model_generator macro loops over a list of source columns and emits type-aware casts (e.g. TIMESTAMP columns get an explicit ::varchar cast; everything else passes through).\n\nHand-expand what that macro would generate for `source_a` (columns: id, name, amount, created_at): cast created_at to VARCHAR, and leave id, name, amount as-is.\n\nReturn `id`, `name`, `amount`, `created_at` (as VARCHAR), ordered by `id`.",
    "schemaSql": SCHEMAS.sourceASourceB,
    "solutionSql": "SELECT id, name, amount, created_at::VARCHAR AS created_at FROM source_a ORDER BY id;",
    "hint": "SELECT id, name, amount, created_at::VARCHAR AS created_at FROM source_a",
    "starter": "-- source_a(id, name, amount, created_at)\n",
  },
  {
    "id": "16.2",
    "lesson": 16,
    "difficulty": "hard",
    "title": "Reconciling schema drift before a UNION",
    "concept": "Macro-style force-casting mismatched columns before combining sources",
    "tables": "source_a(id, name, amount, created_at)\nsource_b(id, name, amount_usd VARCHAR, created_ts)",
    "prompt": "`source_a` and `source_b` represent the same logical entity from two systems, but source_b's columns differ in name and type (amount_usd is a VARCHAR that needs casting to a DECIMAL, and it's named differently than amount).\n\nSimilar to this repo's gainsight_union_relations macro (which force-casts mismatched columns before a UNION), write a query combining both sources into consistent output columns `id`, `name`, `amount`, `created_at`, plus a literal `source_system` ('a' or 'b').\n\nOrder by `id`, then `source_system`.",
    "schemaSql": SCHEMAS.sourceASourceB,
    "solutionSql": "SELECT id, name, amount, created_at::VARCHAR AS created_at, 'a' AS source_system FROM source_a\nUNION ALL\nSELECT id, name, amount_usd::DECIMAL(10,2) AS amount, created_ts::VARCHAR AS created_at, 'b' AS source_system FROM source_b\nORDER BY id, source_system;",
    "hint": "Cast amount_usd::DECIMAL(10,2) AS amount and created_ts::VARCHAR AS created_at in the source_b branch, then UNION ALL with matching column names.",
    "starter": "-- source_a(id, name, amount, created_at)\n-- source_b(id, name, amount_usd, created_ts)\n",
  },
  {
    "id": "16.3",
    "lesson": 16,
    "difficulty": "hard",
    "title": "Introspecting column metadata",
    "concept": "What adapter.get_columns_in_relation() effectively surfaces",
    "tables": "columns_metadata(column_name, data_type)",
    "prompt": "Macros that generate SQL dynamically usually start by introspecting a relation's columns (like adapter.get_columns_in_relation). `columns_metadata` simulates that introspection result.\n\nReturn, for each `data_type` present, the count of columns with that type (alias `column_count`).\n\nOrder by `data_type`.",
    "schemaSql": SCHEMAS.sourceASourceB,
    "solutionSql": "SELECT data_type, COUNT(*) AS column_count FROM columns_metadata GROUP BY data_type ORDER BY data_type;",
    "hint": "GROUP BY data_type, COUNT(*) AS column_count",
    "starter": "-- columns_metadata(column_name, data_type)\n",
  },
  {
    "id": "16.4",
    "lesson": 16,
    "difficulty": "hard",
    "title": "Replicating a Jinja if/else branch in SQL",
    "concept": "CASE WHEN as the SQL-side analog of a Jinja {% if %} branch",
    "tables": "columns_metadata(column_name, data_type)",
    "prompt": "A macro's Jinja loop often does: {% if column.dtype == 'TIMESTAMP_TZ' %}{{ column }}::timestamp_ntz{% else %}{{ column }}{% endif %}.\n\nFor each row in `columns_metadata`, return `column_name` and a computed `cast_expression` string: if data_type = 'TIMESTAMP_TZ', return '<column_name>::timestamp_ntz'; otherwise just '<column_name>'.\n\nOrder by `column_name`.",
    "schemaSql": SCHEMAS.sourceASourceB,
    "solutionSql": "SELECT column_name, CASE WHEN data_type = 'TIMESTAMP_TZ' THEN column_name || '::timestamp_ntz' ELSE column_name END AS cast_expression FROM columns_metadata ORDER BY column_name;",
    "hint": "CASE WHEN data_type = 'TIMESTAMP_TZ' THEN column_name || '::timestamp_ntz' ELSE column_name END AS cast_expression",
    "starter": "-- columns_metadata(column_name, data_type)\n",
  },
  {
    "id": "16.5",
    "lesson": 16,
    "difficulty": "hard",
    "title": "Capstone: reconcile then dedupe",
    "concept": "UNION reconciliation (16.2) + QUALIFY dedup (lesson 8/13)",
    "tables": "source_a, source_b",
    "prompt": "Combine `source_a` and `source_b` into one reconciled dataset (as in 16.2), then keep only the latest row per id (by created_at), in case the same id exists in both sources.\n\nReturn `id`, `name`, `amount`, `created_at`, `source_system`, ordered by `id`.",
    "schemaSql": SCHEMAS.sourceASourceB,
    "solutionSql": "WITH combined AS (\n  SELECT id, name, amount, created_at::VARCHAR AS created_at, 'a' AS source_system FROM source_a\n  UNION ALL\n  SELECT id, name, amount_usd::DECIMAL(10,2) AS amount, created_ts::VARCHAR AS created_at, 'b' AS source_system FROM source_b\n)\nSELECT id, name, amount, created_at, source_system\nFROM combined\nQUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at DESC) = 1\nORDER BY id;",
    "hint": "Put the 16.2 UNION ALL in a combined CTE, then QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at DESC) = 1 in the outer select.",
    "starter": "-- source_a(id, name, amount, created_at)\n-- source_b(id, name, amount_usd, created_ts)\n",
  },
  {
    "id": "17.1",
    "lesson": 17,
    "difficulty": "hard",
    "title": "COALESCE fallback join keys",
    "concept": "Joining when neither side reliably has a single populated key",
    "tables": "accounts_multi(account_key, accountid_a, accountid_b, account_name)\nterritory_plan(plan_id, accountid_a, accountid_b, territory, priority)",
    "prompt": "Two systems can identify the same account by either `accountid_a` or `accountid_b` -- never both reliably populated on both sides. This repo's models constantly bridge that gap with a fallback-key join pattern.\n\nJoin `territory_plan` to `accounts_multi` using that fallback-key approach, matching on whichever id is populated on each side. Return `account_name`, `territory`, `plan_id`.\n\nOrder by `plan_id`.",
    "schemaSql": SCHEMAS.accountsMultiTerritoryPlan,
    "solutionSql": "SELECT a.account_name, t.territory, t.plan_id FROM territory_plan t JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b) ORDER BY t.plan_id;",
    "hint": "JOIN territory_plan t ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)",
    "starter": "-- accounts_multi(account_key, accountid_a, accountid_b, account_name)\n-- territory_plan(plan_id, accountid_a, accountid_b, territory, priority)\n",
  },
  {
    "id": "17.2",
    "lesson": 17,
    "difficulty": "hard",
    "title": "QUALIFY tie-break on duplicate matches",
    "concept": "DENSE_RANK() ... QUALIFY = 1, as in rev_sales_territory_planning",
    "tables": "accounts_multi, territory_plan (with a genuine duplicate match)",
    "prompt": "Data quality issues mean a single account can match more than one territory_plan row (check the sample data -- Acme Corp matches two rows). Keep only the highest-priority (lowest priority number) territory row per account, reusing the join from 17.1.\n\nReturn `account_name`, `territory`, `plan_id`, `priority`, ordered by `account_name`.",
    "schemaSql": SCHEMAS.accountsMultiTerritoryPlan,
    "solutionSql": "SELECT a.account_name, t.territory, t.plan_id, t.priority\nFROM territory_plan t\nJOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)\nQUALIFY DENSE_RANK() OVER (PARTITION BY COALESCE(a.accountid_a, a.accountid_b) ORDER BY t.priority) = 1\nORDER BY a.account_name;",
    "hint": "QUALIFY DENSE_RANK() OVER (PARTITION BY COALESCE(a.accountid_a, a.accountid_b) ORDER BY t.priority) = 1",
    "starter": "-- accounts_multi(account_key, accountid_a, accountid_b, account_name)\n-- territory_plan(plan_id, accountid_a, accountid_b, territory, priority)\n",
  },
  {
    "id": "17.3",
    "lesson": 17,
    "difficulty": "hard",
    "title": "A third source, LEFT JOINed with COALESCE defaults",
    "concept": "Multi-CTE layered joins across three sources",
    "tables": "accounts_multi, territory_plan, web_contracts(contract_id, accountid_a, contract_value)",
    "prompt": "Build a query with three CTEs: `acct` (accounts_multi), `territory` (the deduped territory_plan logic from 17.2, projecting account_key and territory), and `contracts` (web_contracts, keyed only by accountid_a).\n\nCombine all three so every account appears even without a territory or contract match. Return `account_name`, `territory` (NULL if none), and `contract_value` (0 if none).\n\nOrder by `account_name`.",
    "schemaSql": SCHEMAS.accountsMultiTerritoryPlan,
    "solutionSql": "WITH acct AS (SELECT * FROM accounts_multi),\nterritory AS (\n  SELECT a.account_key, t.territory\n  FROM territory_plan t\n  JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)\n  QUALIFY DENSE_RANK() OVER (PARTITION BY a.account_key ORDER BY t.priority) = 1\n),\ncontracts AS (SELECT * FROM web_contracts)\nSELECT acct.account_name,\n       territory.territory,\n       COALESCE(contracts.contract_value, 0) AS contract_value\nFROM acct\nLEFT JOIN territory ON territory.account_key = acct.account_key\nLEFT JOIN contracts ON contracts.accountid_a = acct.accountid_a\nORDER BY acct.account_name;",
    "hint": "Three CTEs (acct, territory, contracts), two LEFT JOINs off acct, COALESCE(contracts.contract_value, 0).",
    "starter": "-- accounts_multi(account_key, accountid_a, accountid_b, account_name)\n-- territory_plan(plan_id, accountid_a, accountid_b, territory, priority)\n-- web_contracts(contract_id, accountid_a, contract_value)\n",
  },
  {
    "id": "17.4",
    "lesson": 17,
    "difficulty": "hard",
    "title": "Appending metadata columns",
    "concept": "This repo's habit of appending table_owner / load_date in the final select",
    "tables": "same as 10.3",
    "prompt": "Models here habitually append metadata columns at the end of the final select (table_owner, load_date).\n\nTake the join logic from 17.3 and add two literal columns: `table_owner` = 'analytics_eng' and `load_date` = DATE '2024-06-01' (standing in for CURRENT_DATE in this exercise).\n\nReturn `account_name`, `territory`, `contract_value`, `table_owner`, `load_date`, ordered by `account_name`.",
    "schemaSql": SCHEMAS.accountsMultiTerritoryPlan,
    "solutionSql": "WITH acct AS (SELECT * FROM accounts_multi),\nterritory AS (\n  SELECT a.account_key, t.territory\n  FROM territory_plan t\n  JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)\n  QUALIFY DENSE_RANK() OVER (PARTITION BY a.account_key ORDER BY t.priority) = 1\n),\ncontracts AS (SELECT * FROM web_contracts)\nSELECT acct.account_name,\n       territory.territory,\n       COALESCE(contracts.contract_value, 0) AS contract_value\n       , 'analytics_eng' AS table_owner\n       , DATE '2024-06-01' AS load_date\nFROM acct\nLEFT JOIN territory ON territory.account_key = acct.account_key\nLEFT JOIN contracts ON contracts.accountid_a = acct.accountid_a\nORDER BY acct.account_name;",
    "hint": "Reuse 17.3 and append , 'analytics_eng' AS table_owner and , DATE '2024-06-01' AS load_date to the final select list.",
    "starter": "-- accounts_multi(account_key, accountid_a, accountid_b, account_name)\n-- territory_plan(plan_id, accountid_a, accountid_b, territory, priority)\n-- web_contracts(contract_id, accountid_a, contract_value)\n",
  },
  {
    "id": "17.5",
    "lesson": 17,
    "difficulty": "hard",
    "title": "Grand capstone: the full pipeline",
    "concept": "Everything in this lesson, combined",
    "tables": "same as 10.3/10.4",
    "prompt": "Bring it all together: for each account, return `account_name`, `territory` (top-priority), `contract_value` (defaulted to 0), a computed `account_tier` column ('key_account' when contract_value > 4000, else 'standard'), and the literal `table_owner` = 'analytics_eng'.\n\nOrder by `contract_value` descending.",
    "schemaSql": SCHEMAS.accountsMultiTerritoryPlan,
    "solutionSql": "WITH acct AS (SELECT * FROM accounts_multi),\nterritory AS (\n  SELECT a.account_key, t.territory\n  FROM territory_plan t\n  JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)\n  QUALIFY DENSE_RANK() OVER (PARTITION BY a.account_key ORDER BY t.priority) = 1\n),\ncontracts AS (SELECT * FROM web_contracts)\nSELECT acct.account_name,\n       territory.territory,\n       COALESCE(contracts.contract_value, 0) AS contract_value,\n       CASE WHEN COALESCE(contracts.contract_value, 0) > 4000 THEN 'key_account' ELSE 'standard' END AS account_tier,\n       'analytics_eng' AS table_owner\nFROM acct\nLEFT JOIN territory ON territory.account_key = acct.account_key\nLEFT JOIN contracts ON contracts.accountid_a = acct.accountid_a\nORDER BY contract_value DESC;",
    "hint": "Same three CTEs as 17.3/17.4, plus a CASE on COALESCE(contracts.contract_value, 0) for account_tier.",
    "starter": "-- accounts_multi(account_key, accountid_a, accountid_b, account_name)\n-- territory_plan(plan_id, accountid_a, accountid_b, territory, priority)\n-- web_contracts(contract_id, accountid_a, contract_value)\n",
  },
  {
    "id": "18.1",
    "lesson": 18,
    "difficulty": "hard",
    "title": "Walking an Org Chart with WITH RECURSIVE",
    "concept": "WITH RECURSIVE basic depth",
    "tables": "employees(employee_id, employee_name, manager_id)",
    "prompt": "`employees.manager_id` points to another employee's `employee_id`; the top of the org (the CEO) has a null `manager_id`. Write a `with recursive` CTE that walks down the hierarchy from the CEO, computing each employee's `depth` (0 for the CEO, incrementing by one per level down). Return `employee_id`, `employee_name`, and `depth`. Order by `depth`, `employee_id`.",
    "schemaSql": SCHEMAS.employees3,
    "solutionSql": "with recursive org_chart as (\n    select\n        employee_id\n      , employee_name\n      , manager_id\n      , 0 as depth\n    from employees\n    where manager_id is null\n\n    union all\n\n    select\n        e.employee_id\n      , e.employee_name\n      , e.manager_id\n      , o.depth + 1 as depth\n    from employees as e\n    inner join org_chart as o\n      on e.manager_id = o.employee_id\n)\nselect\n    employee_id\n  , employee_name\n  , depth\nfrom org_chart\norder by depth, employee_id",
    "hint": "Anchor member: `where manager_id is null` with `depth = 0`. Recursive member: join `employees` back to the CTE on `e.manager_id = o.employee_id`, `depth + 1`.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n",
  },
  {
    "id": "18.2",
    "lesson": 18,
    "difficulty": "hard",
    "title": "Building a Path String Recursively",
    "concept": "recursive CTE + path building",
    "tables": "employees(employee_id, employee_name, manager_id)",
    "prompt": "Extend the org-chart recursion to also build a `path` string showing the chain of names from the top down, e.g. `'Priya > Sam > Noor'`. Return `employee_id`, `employee_name`, and `path`. Order by `path`.",
    "schemaSql": SCHEMAS.employees4,
    "solutionSql": "with recursive org_chart as (\n    select\n        employee_id\n      , employee_name\n      , manager_id\n      , employee_name as path\n    from employees\n    where manager_id is null\n\n    union all\n\n    select\n        e.employee_id\n      , e.employee_name\n      , e.manager_id\n      , o.path || ' > ' || e.employee_name as path\n    from employees as e\n    inner join org_chart as o\n      on e.manager_id = o.employee_id\n)\nselect\n    employee_id\n  , employee_name\n  , path\nfrom org_chart\norder by path",
    "hint": "Anchor `path = employee_name`; recursive step concatenates `o.path || ' > ' || e.employee_name`.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n",
  },
  {
    "id": "18.3",
    "lesson": 18,
    "difficulty": "hard",
    "title": "Counting Descendants with a Recursive CTE",
    "concept": "recursive CTE + aggregation",
    "tables": "employees(employee_id, employee_name, manager_id)",
    "prompt": "Build a recursive CTE that, starting from each employee, walks down to every descendant (direct and indirect report), producing one row per (ancestor `employee_id`, descendant `employee_id`) pair. Then aggregate to return each `employee_id`, `employee_name`, and `descendant_count` -- the number of descendants found for them (0 if they have none).\n\nOrder by `employee_id`.",
    "schemaSql": SCHEMAS.employees1,
    "solutionSql": "with recursive descendants as (\n    select\n        employee_id as ancestor_id\n      , employee_id as descendant_id\n    from employees\n\n    union all\n\n    select\n        d.ancestor_id\n      , e.employee_id as descendant_id\n    from employees as e\n    inner join descendants as d\n      on e.manager_id = d.descendant_id\n)\nselect\n    e.employee_id\n  , e.employee_name\n  , count(d.descendant_id) filter (where d.descendant_id != d.ancestor_id) as descendant_count\nfrom employees as e\nleft join descendants as d\n  on e.employee_id = d.ancestor_id\ngroup by e.employee_id, e.employee_name\norder by e.employee_id",
    "hint": "Seed `descendants` with each employee as their own ancestor/descendant, recurse down via `manager_id`, then `count(...) filter (where descendant_id != ancestor_id)` to exclude self-counting.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n",
  },
  {
    "id": "18.4",
    "lesson": 18,
    "difficulty": "hard",
    "title": "Limiting Recursion Depth",
    "concept": "recursive CTE with depth cutoff",
    "tables": "employees(employee_id, employee_name, manager_id)",
    "prompt": "Walk the org chart recursively as before, but this time limit the result to just the top of the org (depth 0) and their direct reports (depth 1) \u2014 nobody deeper. Return `employee_id`, `employee_name`, `depth`. Order by `depth`, `employee_id`.",
    "schemaSql": SCHEMAS.employees3,
    "solutionSql": "with recursive org_chart as (\n    select\n        employee_id\n      , employee_name\n      , manager_id\n      , 0 as depth\n    from employees\n    where manager_id is null\n\n    union all\n\n    select\n        e.employee_id\n      , e.employee_name\n      , e.manager_id\n      , o.depth + 1 as depth\n    from employees as e\n    inner join org_chart as o\n      on e.manager_id = o.employee_id\n    where o.depth < 1\n)\nselect\n    employee_id\n  , employee_name\n  , depth\nfrom org_chart\norder by depth, employee_id",
    "hint": "Add `where o.depth < 1` to the recursive member (the second half of the `union all`), not the final `select`, so recursion itself stops early.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n",
  },
  {
    "id": "18.5",
    "lesson": 18,
    "difficulty": "hard",
    "title": "Capstone: Full Hierarchy Report",
    "concept": "recursive CTE: depth + path + manager name",
    "tables": "employees(employee_id, employee_name, manager_id)",
    "prompt": "Produce a full hierarchy report combining everything from this lesson: a recursive CTE returning `employee_id`, `employee_name`, `depth` (0 at the top, incrementing per level), and `path` (names joined with `' > '` from the top down). Then, in the final select, also attach each employee's `manager_name` (null at the top). Order by `path`.",
    "schemaSql": SCHEMAS.employees4,
    "solutionSql": "with recursive org_chart as (\n    select\n        employee_id\n      , employee_name\n      , manager_id\n      , 0 as depth\n      , employee_name as path\n    from employees\n    where manager_id is null\n\n    union all\n\n    select\n        e.employee_id\n      , e.employee_name\n      , e.manager_id\n      , o.depth + 1 as depth\n      , o.path || ' > ' || e.employee_name as path\n    from employees as e\n    inner join org_chart as o\n      on e.manager_id = o.employee_id\n)\nselect\n    org_chart.employee_id\n  , org_chart.employee_name\n  , org_chart.depth\n  , org_chart.path\n  , m.employee_name as manager_name\nfrom org_chart\nleft join employees as m\n  on org_chart.manager_id = m.employee_id\norder by path",
    "hint": "Build `depth` and `path` inside the recursive CTE as in modules 18.1/18.2, then `left join` the CTE's output back to plain `employees` for `manager_name`.",
    "starter": "-- employees(employee_id, employee_name, manager_id)\n",
  },
  {
    "id": "19.1",
    "lesson": 19,
    "difficulty": "hard",
    "title": "Packing Columns into a Struct",
    "concept": "struct_pack",
    "tables": "customers(customer_id, first_name, last_name, email)",
    "prompt": "This is the inverse of flattening: building nested structure out of flat rows. Return `customer_id` and a single nested column, aliased `contact_info`, that packs together each customer's `first_name`, `last_name`, and `email` into one struct-like value. Order by `customer_id`.",
    "schemaSql": SCHEMAS.customers3,
    "solutionSql": "select\n    customer_id\n  , struct_pack(first_name := first_name, last_name := last_name, email := email) as contact_info\nfrom customers\norder by customer_id",
    "hint": "`struct_pack(first_name := first_name, last_name := last_name, email := email)` -- the `:=` names each struct field.",
    "starter": "-- customers(customer_id, first_name, last_name, email)\n",
  },
  {
    "id": "19.2",
    "lesson": 19,
    "difficulty": "hard",
    "title": "Converting a Struct to JSON",
    "concept": "to_json(struct)",
    "tables": "orders(order_id, customer_id, amount, status)",
    "prompt": "Build a JSON payload per order containing its `order_id`, `amount`, and `status`. Return `order_id` and the JSON payload aliased `order_json`. Order by `order_id`.",
    "schemaSql": SCHEMAS.orders5,
    "solutionSql": "select\n    order_id\n  , to_json(\n      struct_pack(order_id := order_id, amount := amount, status := status)\n    ) as order_json\nfrom orders\norder by order_id",
    "hint": "`to_json(struct_pack(order_id := order_id, amount := amount, status := status))`.",
    "starter": "-- orders(order_id, customer_id, amount, status)\n",
  },
  {
    "id": "19.3",
    "lesson": 19,
    "difficulty": "hard",
    "title": "Building a JSON Array with ARRAY_AGG",
    "concept": "array_agg + to_json (JSON array)",
    "tables": "order_items(order_id, product_name, quantity)",
    "prompt": "For each `order_id`, build a JSON array containing that order's item quantities, ordered by `product_name` for a deterministic result. Group by `order_id` and return `order_id` and the JSON array aliased `quantities_json`.\n\nOrder by `order_id`.",
    "schemaSql": SCHEMAS.orderItems,
    "solutionSql": "select\n    order_id\n  , to_json(array_agg(quantity order by product_name)) as quantities_json\nfrom order_items\ngroup by order_id\norder by order_id",
    "hint": "`to_json(array_agg(quantity order by product_name))` -- ordering inside `array_agg` keeps the array deterministic.",
    "starter": "-- order_items(order_id, product_name, quantity)\n",
  },
  {
    "id": "19.4",
    "lesson": 19,
    "difficulty": "hard",
    "title": "Nesting Structs into a JSON Array of Objects",
    "concept": "array_agg(struct_pack) + to_json",
    "tables": "order_items(order_id, product_name, quantity)",
    "prompt": "Go one level deeper: for each `order_id`, build a JSON array where each element is an object containing that item's `product_name` and `quantity` (not just the raw quantity). Order the elements within each array by `product_name` for a deterministic result. Return `order_id` and `items_json`.\n\nOrder by `order_id`.",
    "schemaSql": SCHEMAS.orderItems1,
    "solutionSql": "select\n    order_id\n  , to_json(\n      array_agg(\n        struct_pack(product_name := product_name, quantity := quantity)\n        order by product_name\n      )\n    ) as items_json\nfrom order_items\ngroup by order_id\norder by order_id",
    "hint": "Nest three calls: `to_json(array_agg(struct_pack(product_name := product_name, quantity := quantity) order by product_name))`.",
    "starter": "-- order_items(order_id, product_name, quantity)\n",
  },
  {
    "id": "19.5",
    "lesson": 19,
    "difficulty": "hard",
    "title": "Capstone: Nested Customer Payload with Orders Array",
    "concept": "join + array_agg(struct_pack) + to_json capstone",
    "tables": "customers(customer_id, customer_name)\norders(order_id, customer_id, amount)",
    "prompt": "Build one JSON payload per customer containing their nested list of orders. Join `customers` to `orders`, group by `customer_id` and `customer_name`, and return `customer_id`, `customer_name`, and `orders_json` \u2014 a JSON array where each element has that order's `order_id` and `amount`, ordered by `order_id` within each customer. Order by `customer_id`.",
    "schemaSql": SCHEMAS.customersOrders3,
    "solutionSql": "select\n    c.customer_id\n  , c.customer_name\n  , to_json(\n      array_agg(\n        struct_pack(order_id := o.order_id, amount := o.amount)\n        order by o.order_id\n      )\n    ) as orders_json\nfrom customers as c\ninner join orders as o\n  on c.customer_id = o.customer_id\ngroup by c.customer_id, c.customer_name\norder by c.customer_id",
    "hint": "Join first, then `group by customer_id, customer_name`, and wrap `array_agg(struct_pack(order_id := o.order_id, amount := o.amount) order by o.order_id)` in `to_json(...)`.",
    "starter": "-- customers(customer_id, customer_name)\n  -- orders(order_id, customer_id, amount)\n",
  },
  {
    "id": "20.1",
    "lesson": 20,
    "difficulty": "hard",
    "title": "Pivoting with Conditional Aggregation",
    "concept": "SUM(CASE WHEN...) pivot",
    "tables": "orders(order_id, region, amount)",
    "prompt": "Build a pivot-style report with one row total and one column per region. Return a single row with `west_total`, `east_total`, and `north_total`, each holding the total `amount` for that region.",
    "schemaSql": SCHEMAS.orders6,
    "solutionSql": "select\n    sum(case when region = 'west' then amount else 0 end) as west_total\n  , sum(case when region = 'east' then amount else 0 end) as east_total\n  , sum(case when region = 'north' then amount else 0 end) as north_total\nfrom orders",
    "hint": "Each pivoted column is its own `sum(case when region = '<x>' then amount else 0 end)` in the same select list.",
    "starter": "-- orders(order_id, region, amount)\n",
  },
  {
    "id": "20.2",
    "lesson": 20,
    "difficulty": "hard",
    "title": "Pivoting with DuckDB's PIVOT Statement",
    "concept": "PIVOT ... ON ... USING",
    "tables": "orders(order_id, region, amount)",
    "prompt": "Rebuild the same region pivot using DuckDB's `pivot` statement.\n\nNote: DuckDB's `pivot` auto-groups by any source column not used in `on`/`using`, so make sure you're only pivoting the columns relevant to the result (not `order_id`).\n\nProduce a single row with a column per distinct `region` value holding the summed `amount`.",
    "schemaSql": SCHEMAS.orders6,
    "solutionSql": "pivot (select region, amount from orders)\non region\nusing sum(amount)",
    "hint": "DuckDB syntax: `pivot (select region, amount from orders) on region using sum(amount)` -- dropping `order_id` from the subquery avoids it becoming an implicit group-by column.",
    "starter": "-- orders(order_id, region, amount)\n",
  },
  {
    "id": "20.3",
    "lesson": 20,
    "difficulty": "hard",
    "title": "Conditional Aggregation with a Grouping Column",
    "concept": "SUM(CASE WHEN...) with GROUP BY",
    "tables": "orders(order_id, customer_id, channel, amount)",
    "prompt": "Return one row per `customer_id` with `online_total` and `retail_total`, each the sum of `amount` for that `channel` ('online' or 'retail' respectively), grouping by `customer_id`. Order by `customer_id`.",
    "schemaSql": SCHEMAS.orders7,
    "solutionSql": "select\n    customer_id\n  , sum(case when channel = 'online' then amount else 0 end) as online_total\n  , sum(case when channel = 'retail' then amount else 0 end) as retail_total\nfrom orders\ngroup by customer_id\norder by customer_id",
    "hint": "`group by customer_id` with two `sum(case when channel = '<x>' then amount else 0 end)` columns.",
    "starter": "-- orders(order_id, customer_id, channel, amount)\n",
  },
  {
    "id": "20.4",
    "lesson": 20,
    "difficulty": "hard",
    "title": "Combining Aggregation with a Window Frame",
    "concept": "ROWS BETWEEN window frame",
    "tables": "daily_sales(sale_date, region, amount)",
    "prompt": "Return `sale_date`, `region`, `amount`, and a `trailing_3day_total` per `region` that sums `amount` over the current row and the 2 preceding rows, ordered by `sale_date`. Order by `region`, `sale_date`.",
    "schemaSql": SCHEMAS.dailySales,
    "solutionSql": "select\n    sale_date\n  , region\n  , amount\n  , sum(amount) over (\n      partition by region order by sale_date\n      rows between 2 preceding and current row\n    ) as trailing_3day_total\nfrom daily_sales\norder by region, sale_date",
    "hint": "`sum(amount) over (partition by region order by sale_date rows between 2 preceding and current row)`.",
    "starter": "-- daily_sales(sale_date, region, amount)\n",
  },
  {
    "id": "20.5",
    "lesson": 20,
    "difficulty": "hard",
    "title": "Capstone: Pivoted Channel Totals with a Trailing Window",
    "concept": "conditional aggregation pivot + ROWS BETWEEN capstone",
    "tables": "daily_sales(sale_date, channel, amount)",
    "prompt": "Build a capstone report combining both ideas from this lesson. First compute, per `sale_date`, the conditional-aggregation pivot columns `online_total` and `retail_total`, grouped by `sale_date`, in a CTE named `daily_totals`. Then, in the final select, add a `trailing_online_3day` window column that sums `online_total` over the current row and the 2 preceding rows, ordered by `sale_date`. Return `sale_date`, `online_total`, `retail_total`, `trailing_online_3day`. Order by `sale_date`.",
    "schemaSql": SCHEMAS.dailySales1,
    "solutionSql": "with daily_totals as (\n    select\n        sale_date\n      , sum(case when channel = 'online' then amount else 0 end) as online_total\n      , sum(case when channel = 'retail' then amount else 0 end) as retail_total\n    from daily_sales\n    group by sale_date\n)\nselect\n    sale_date\n  , online_total\n  , retail_total\n  , sum(online_total) over (\n      order by sale_date\n      rows between 2 preceding and current row\n    ) as trailing_online_3day\nfrom daily_totals\norder by sale_date",
    "hint": "Build `daily_totals` as a CTE with the two conditional sums grouped by `sale_date`, then apply `sum(online_total) over (order by sale_date rows between 2 preceding and current row)` in the outer select.",
    "starter": "-- daily_sales(sale_date, channel, amount)\n",
  },
];

export { LESSONS, MODULES };
