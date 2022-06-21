create or replace view v_acl_permission
as
with recursive acl_permission_tree as
( select ap.id as permission_id
       , ap.key
       , ap.parent_id
       , ap.description
       , lpad(ap.seq_no::text, 3, '0') as _seq_no
       , ap.seq_no
    from acl_permission ap
    where ap.parent_id is null
  union all
  select ap.id
       , apt.key || '.' || ap.key
       , ap.parent_id
       , apt.description || ' - ' || ap.description
       , apt._seq_no || '.' || lpad(ap.seq_no::text, 3, '0')
       , ap.seq_no
    from acl_permission ap join acl_permission_tree apt on ap.parent_id = apt.permission_id
), acl_permission_with_children as
( select ap.id as permission_id
       , ap.parent_id
       , array[ap.id] as node_with_children
    from acl_permission ap
  union
  select ap.id
       , ap.parent_id
       , ap.id || apwc.node_with_children
    from acl_permission_with_children apwc join acl_permission ap on ap.id = apwc.parent_id
), node_with_children as
( select apwc.permission_id, array_agg(distinct nodes) as nodes
    from acl_permission_with_children apwc
       , unnest(apwc.node_with_children) as nodes
    group by apwc.permission_id
)
select apt.permission_id
     , apt.key
     , apt.description
     , apt.seq_no
     , nwc.nodes as permissions
     , apt._seq_no -- for sorting
  from acl_permission_tree apt
     , node_with_children nwc
  where apt.permission_id = nwc.permission_id;