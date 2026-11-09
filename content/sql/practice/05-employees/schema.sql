CREATE OR REPLACE TABLE employees (
    id INTEGER,
    managerId INTEGER,
    name VARCHAR,
    department VARCHAR,
    salary INTEGER
);
INSERT INTO employees VALUES
 (1, NULL, 'Alice', 'Eng', 180000),
 (2, 1, 'Bob', 'Eng', 140000),
 (3, 1, 'Carol', 'Eng', 145000),
 (4, 2, 'Dave', 'Eng', 150000),
 (5, NULL, 'Erin', 'Sales', 170000),
 (6, 5, 'Frank', 'Sales', 95000),
 (7, 5, 'Grace', 'Sales', 98000),
 (8, 3, 'Heidi', 'Eng', 105000);
