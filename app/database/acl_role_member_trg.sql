create or replace function acl_role_member_before_trigger_fnc() returns trigger
language plpgsql
as $body$
declare
  cur record;
begin
  for cur in
  ( select null
      from v_acl_role_member
      where role_id = NEW.role_id
        and NEW.member_role_id = any(roles)
  ) loop
    raise exception 'errors.acl_role_member.cycle';
  end loop;
  return NEW;
end 
$body$;

create or replace trigger acl_role_member_before_trigger
  before update
  on acl_role_member
  for each row
  execute procedure acl_role_member_before_trigger_fnc();