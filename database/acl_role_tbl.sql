create table if not exists acl_role                -- Роли и пользователи (history)
( id              bigserial not null primary key   -- Уникальный идентификатор
, can_login       boolean   not null default true  -- Разрешен логин? true - пользователь / false - роль
, username        text               unique        -- Имя пользователя
, description     text                             -- Описание
, is_active       boolean   not null default true  -- Статус (true - активен / false - заблокирован)
, is_admin        boolean   not null default false -- Пользователь является администратором?
, hashed_password text                             -- Пароль (алгоритм согласно конфигурации)
);

call create_history('acl_role', array['hashed_password']);