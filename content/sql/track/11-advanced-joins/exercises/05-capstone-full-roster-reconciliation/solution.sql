select
    coalesce(e.employee_id, p.employee_id) as employee_id
  , e.employee_name
  , m.employee_name as manager_name
  , p.salary
from employees as e
full outer join payroll_records as p
  on e.employee_id = p.employee_id
left join employees as m
  on e.manager_id = m.employee_id
order by employee_id
