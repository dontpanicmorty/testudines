with recursive org_chart as (
    select
        employee_id
      , employee_name
      , manager_id
      , employee_name as path
    from employees
    where manager_id is null

    union all

    select
        e.employee_id
      , e.employee_name
      , e.manager_id
      , o.path || ' > ' || e.employee_name as path
    from employees as e
    inner join org_chart as o
      on e.manager_id = o.employee_id
)
select
    employee_id
  , employee_name
  , path
from org_chart
order by path
