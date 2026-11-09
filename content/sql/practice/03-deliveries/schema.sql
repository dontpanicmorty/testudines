CREATE OR REPLACE TABLE deliveries_info (
    delivery_id INTEGER,
    user_id INTEGER,
    delivery_date DATE,
    delivery_week DATE,
    route_id INTEGER,
    delivery_success_flag BOOLEAN
);
INSERT INTO deliveries_info VALUES
 (1,1,'2026-01-05','2026-01-05',10,true),
 (2,1,'2026-01-08','2026-01-05',10,true),
 (3,2,'2026-01-05','2026-01-05',11,false),
 (4,2,'2026-01-08','2026-01-05',11,true),
 (5,1,'2026-01-12','2026-01-12',10,true),
 (6,3,'2026-01-12','2026-01-12',12,true),
 (7,3,'2026-01-15','2026-01-12',12,true),
 (8,2,'2026-01-19','2026-01-19',11,true),
 (9,1,'2026-01-19','2026-01-19',10,false),
 (10,4,'2026-01-22','2026-01-19',13,true);
