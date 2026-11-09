CREATE OR REPLACE TABLE regions(id INTEGER, name VARCHAR);
INSERT INTO regions VALUES (1,'North'),(2,'South'),(3,'East'),(4,'West'),(5,'Midwest');

CREATE OR REPLACE TABLE states(id INTEGER, name VARCHAR, regionId INTEGER);
INSERT INTO states VALUES
 (1,'Minnesota',1),(2,'Texas',2),(3,'California',3),(4,'Columbia',4),(5,'Indiana',5);

CREATE OR REPLACE TABLE employees(id INTEGER, name VARCHAR, stateId INTEGER);
INSERT INTO employees VALUES
 (1,'Jaden',1),(2,'Abby',1),(3,'Amaya',2),(4,'Robert',3),(5,'Tom',4),(6,'William',5);

CREATE OR REPLACE TABLE sales(id INTEGER, amount INTEGER, employeeId INTEGER);
INSERT INTO sales VALUES
 (1,2000,1),(2,3000,2),(3,4000,3),(4,1200,4),(5,2400,5),(6,500,1),(7,1800,3);
