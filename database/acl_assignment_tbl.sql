create table if not exists acl_assignment                      -- Выданные права
( role_id       bigint  not null references acl_role(id)       -- Роль
, permission_id bigint  not null references acl_permission(id) -- Право
, primary key (role_id, permission_id)
);

create index if not exists acl_assignment_role_id_idx on acl_assignment(role_id);
create index if not exists acl_assignmenton_permission_id_idx acl_assignment(permission_id);

call create_history('acl_assignment');