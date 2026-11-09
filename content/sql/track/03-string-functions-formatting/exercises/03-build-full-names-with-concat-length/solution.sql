select
    employee_id
  , concat(first_name, ' ', last_name) as full_name
  , length(concat(first_name, ' ', last_name)) as name_length
from employees
order by employee_id
