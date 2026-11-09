SELECT customer_id, first_name, COALESCE(referral_source, 'organic') AS referral_source_final FROM customers ORDER BY customer_id;
