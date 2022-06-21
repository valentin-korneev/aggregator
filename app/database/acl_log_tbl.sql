create table if not exists acl_log                           -- Лог запросов
( role_id       bigint    not null references acl_role(id)   -- Уникальный идентификатор пользователя
, uri_path      text      not null                           -- URI
, request_data  text                                         -- Тело запроса
, response_data text                                         -- Тело ответа
, status_code   integer   not null                           -- Код ответа
, request_time  timestamp not null                           -- Время запроса
, response_time timestamp not null default current_timestamp -- Время ответа
);