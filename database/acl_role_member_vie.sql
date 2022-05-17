create or replace view v_acl_role_member
as
with recursive role_member as
( select r.id as role_id
       , rm.member_role_id
       , r.is_admin
    from acl_role r left join acl_role_member rm on r.id = rm.role_id
), role_member_with_parents as (
  select rm.role_id
       , rm.member_role_id
       , rm.is_admin
       , array[rm.role_id] as member_with_parents
       , rm.is_admin as is_role_admin
    from role_member rm
  union
  select rm.role_id
       , rm.member_role_id
       , rmwp.is_admin or rm.is_admin
       , rmwp.member_with_parents || rm.role_id
       , rm.is_admin
  from role_member_with_parents rmwp join role_member rm on rmwp.member_role_id = rm.role_id
)
select rmwp.role_id
     , array_agg(distinct roles) as roles
     , bool_or(rmwp.is_admin) as is_admin
     , not rmwp.is_role_admin and bool_or(rmwp.is_admin) as is_inherit
  from role_member_with_parents rmwp
     , unnest(rmwp.member_with_parents) as roles
  group by rmwp.role_id, rmwp.is_role_admin;