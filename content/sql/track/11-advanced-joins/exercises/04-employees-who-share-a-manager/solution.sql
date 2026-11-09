select
    e1.employee_name as employee_a
  , e2.employee_name as employee_b
from employees as e1
inner join employees as e2
  on e1.manager_id = e2.manager_id
 and e1.employee_id < e2.employee_id
order by employee_a, employee_b
