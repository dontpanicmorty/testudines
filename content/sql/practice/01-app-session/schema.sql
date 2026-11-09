CREATE OR REPLACE TABLE sessions (
    id INTEGER,
    userId INTEGER,
    deviceType VARCHAR,
    duration DECIMAL(10,2),
    sessionDate DATE
);
INSERT INTO sessions VALUES
 (1, 1, 'mobile', 10.0, '2026-01-01'),
 (2, 2, 'desktop', 18.0, '2026-01-01'),
 (3, 1, 'mobile', 14.0, '2026-01-03'),
 (4, 3, 'mobile', 5.0, '2026-01-04'),
 (5, 2, 'desktop', 22.0, '2026-01-05'),
 (6, 1, 'desktop', 30.0, '2026-01-06'),
 (7, 4, 'mobile', 2.0, '2026-01-06'),
 (8, 2, 'mobile', 9.5, '2026-01-07'),
 (9, 3, 'desktop', 40.0, '2026-01-08'),
 (10, 1, 'mobile', 6.0, '2026-01-09');
