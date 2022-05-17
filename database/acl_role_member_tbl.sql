create table if not exists acl_role_member               -- Вхождение ролей друг в друга
( role_id        bigint not null references acl_role(id) -- Роль родитель
, member_role_id bigint not null references acl_role(id) -- Роль наследник
, primary key (role_id, member_role_id)
);

create index if not exists on acl_role_member(role_id);
create index if not exists on acl_role_member(member_role_id);

call create_history('acl_role_member');