SELECT st.name, SUM(sa.amount) AS total_sales FROM states st JOIN employees e ON e.stateId = st.id JOIN sales sa ON sa.employeeId = e.id GROUP BY st.name ORDER BY st.name;
