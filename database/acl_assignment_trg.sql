create or replace function acl_assignment_before_trigger_fnc() returns trigger
language plpgsql
as $body$
declare
  cur record;
begin
  for cur in
  ( select *
      from v_acl_assignment
      where role_id = NEW.role_id
        and permission_id = NEW.permission_id
  ) loop
    if cur.is_admin then
        raise exception 'errors.acl_assignment.admin';
    end if;
    if cur.is_inherit then
        raise exception 'errors.acl_assignment.inherit';
    end if;
  end loop;
  return NEW;
end 
$body$;

create or replace trigger acl_assignment_before_trigger
  before insert or update
  on acl_assignment
  for each row
  execute procedure acl_assignment_before_trigger_fnc();