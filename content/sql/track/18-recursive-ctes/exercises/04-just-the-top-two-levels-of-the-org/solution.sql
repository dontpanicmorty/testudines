with recursive org_chart as (
    select
        employee_id
      , employee_name
      , manager_id
      , 0 as depth
    from employees
    where manager_id is null

    union all

    select
        e.employee_id
      , e.employee_name
      , e.manager_id
      , o.depth + 1 as depth
    from employees as e
    inner join org_chart as o
      on e.manager_id = o.employee_id
    where o.depth < 1
)
select
    employee_id
  , employee_name
  , depth
from org_chart
order by depth, employee_id
