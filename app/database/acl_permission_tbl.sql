create table if not exists acl_permission                      -- Допустимые разрешения
( id          bigserial not null primary key                   -- Уникальный идентификатор
, key         text      not null                               -- Текстовый идентификатор разрешения
, parent_id   bigint             references acl_permission(id) -- Ссылка на родительское разрешение
, description text      not null                               -- Описание
, seq_no      integer   not null default 0                     -- Порядок следования в дереве
);

create index if not exists acl_permission_parent_id_idx on acl_permission(parent_id);
create unique index if not exists acl_permission_key_parent_id_idx on acl_permission(key, coalesce(parent_id, 0));