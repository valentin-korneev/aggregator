create table if not exists acl_token                              -- Токены доступа
( role_id       bigint    not null unique references acl_role(id) -- Уникальный идентификатор пользователя
, access_token  text      not null unique                         -- Токен доступа
, refresh_token text      not null unique                         -- Токен для обновления токена доступа
, changed_at    timestamp not null default current_timestamp      -- Время создания токенов
);