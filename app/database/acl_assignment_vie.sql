create or replace view v_acl_assignment
as
select arm.role_id
     , ap.permission_id
     , ap.key
     , arm.is_admin
     , true as is_inherit
  from v_acl_role_member arm
     , v_acl_permission ap
  where arm.is_admin
union all
select arm.role_id
     , ap.permission_id
     , ap.key
     , arm.is_admin
     , not bool_and(a.role_id = arm.role_id and a.permission_id = ap.permission_id) as is_inherit
  from v_acl_role_member arm
     , acl_assignment a
     , v_acl_permission ap
  where a.role_id = any(arm.roles)
    and a.permission_id = any(ap.permissions)
    and not arm.is_admin
  group by arm.role_id
         , ap.permission_id
         , ap.key
         , arm.is_admin;
 