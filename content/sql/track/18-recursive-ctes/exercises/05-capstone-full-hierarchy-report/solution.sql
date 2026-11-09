with recursive org_chart as (
    select
        employee_id
      , employee_name
      , manager_id
      , 0 as depth
      , employee_name as path
    from employees
    where manager_id is null

    union all

    select
        e.employee_id
      , e.employee_name
      , e.manager_id
      , o.depth + 1 as depth
      , o.path || ' > ' || e.employee_name as path
    from employees as e
    inner join org_chart as o
      on e.manager_id = o.employee_id
)
select
    org_chart.employee_id
  , org_chart.employee_name
  , org_chart.depth
  , org_chart.path
  , m.employee_name as manager_name
from org_chart
left join employees as m
  on org_chart.manager_id = m.employee_id
order by path
