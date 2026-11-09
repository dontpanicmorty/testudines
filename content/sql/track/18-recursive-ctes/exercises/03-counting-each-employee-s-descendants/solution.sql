with recursive descendants as (
    select
        employee_id as ancestor_id
      , employee_id as descendant_id
    from employees

    union all

    select
        d.ancestor_id
      , e.employee_id as descendant_id
    from employees as e
    inner join descendants as d
      on e.manager_id = d.descendant_id
)
select
    e.employee_id
  , e.employee_name
  , count(d.descendant_id) filter (where d.descendant_id != d.ancestor_id) as descendant_count
from employees as e
left join descendants as d
  on e.employee_id = d.ancestor_id
group by e.employee_id, e.employee_name
order by e.employee_id
