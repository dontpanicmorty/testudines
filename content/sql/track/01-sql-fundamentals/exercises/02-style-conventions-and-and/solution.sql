SELECT customer_id, first_name, signup_date FROM customers WHERE region != 'west' AND signup_date >= DATE '2023-01-01' ORDER BY signup_date;
