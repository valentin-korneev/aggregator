create or replace function acl_permission_before_trigger_fnc() returns trigger
language plpgsql
as $body$
declare
  cur record;
begin
  for cur in
  ( select null
      from v_acl_permission
      where permission_id = NEW.id and NEW.parent_id = any(permissions)
  ) loop
    raise exception 'errors.acl_permission.cycle';
  end loop;
  return NEW;
end 
$body$;

create or replace trigger acl_permission_before_trigger
  before update
  on acl_permission
  for each row
  execute procedure acl_permission_before_trigger_fnc();