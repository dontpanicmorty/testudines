select
    e.employee_id
  , e.employee_name
  , m.employee_name as manager_name
from employees as e
left join employees as m
  on e.manager_id = m.employee_id
order by e.employee_id
