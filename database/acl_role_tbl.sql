create table if not exists acl_role                -- Роли и пользователи (history)
( id              bigserial not null primary key   -- Уникальный идентификатор
, can_login       boolean   not null default true  -- Разрешен логин? true - пользователь / false - роль
, username        text               unique        -- Имя пользователя
, description     text                             -- Описание
, is_active       boolean   not null default true  -- Статус (true - активен / false - заблокирован)
, is_admin        boolean   not null default false -- Пользователь является администратором?
, hashed_password text                             -- Пароль (алгоритм согласно конфигурации)
);

do $$
declare
    cur record;
begin
    for cur in (select count(0) as cnt from acl_role) loop
        if cur.cnt = 0 then
            perform set_config('app.private.user_id', '0', true);
            insert into acl_role(id, username, description, is_admin, hashed_password) values(0, 'admin', 'Администратор', true, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');
            insert into acl_role(id, username, can_login, description) values(1, 'public', false, 'Публичный пользователь');
            execute format('alter sequence %s restart with 2', pg_get_serial_sequence('acl_role', 'id'));
        end if;
    end loop; 
end $$;

call create_history('acl_role', array['hashed_password']);