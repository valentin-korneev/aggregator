create or replace procedure create_history(p_table_name text, p_exclude_fields text[] default array[]::text[])
language plpgsql
as $create_history$
declare
  l_table_name_history     text = p_table_name || '_history';
  l_changed_list           text[] := array['changed_by', 'changed_at'];
  l_field_list             text[] := l_changed_list;
  l_primary_key_list       text[];
  l_primary_key_where      text := '';
  l_fields_unchanged       text := '';
  l_rec                    record;  
  l_empty_table            int;
  l_str                    text;
  l_geometric              text[] := array['point', 'line', 'lseg', 'box', 'path', 'path', 'polygon', 'circle'];
  l_network                text[] := array['inet', 'cidr', 'macaddr', 'macaddr8'];
  l_postgres               text[] := array['txid_snapshot', 'pg_snapshot', 'pg_lsn'];
  l_data_types             text[] := array['json', 'xml'];
  l_binary                 text[] := array['bytea'];
  l_invalid_types          text[] := l_geometric || l_network || l_postgres || l_data_types || l_binary;

  -- Ошибка с null в changed_by задумана, чтобы разработчик контролировал выставление своего ID на уровне приложения
  -- select set_config('app.private.user_id', '<ID пользователя>', true);
  l_before_trigger_pattern text := 'create or replace function %1$s_before_trigger_fnc() returns trigger
language plpgsql
as $body$
declare
  l_user_id bigint := nullif(current_setting(''app.private.user_id'', true), '''')::bigint;
begin
  if    TG_OP = ''UPDATE''
%2$s then
    NEW.changed_by := OLD.changed_by;
    NEW.changed_at := OLD.changed_at;
  else
    NEW.changed_by := l_user_id;
    NEW.changed_at := now();
  end if;
  return NEW;
end 
$body$;

create or replace trigger %1$s_before_trigger
  before insert or update
  on %1$s
  for each row
  execute procedure %1$s_before_trigger_fnc();';
  
  l_after_trigger_pattern  text = 'create or replace function %1$s_after_trigger_fnc() returns trigger
language plpgsql
as $body$
declare
  l_user_id bigint := nullif(current_setting(''app.private.user_id'', true), '''')::bigint;
begin
  if    TG_OP = ''UPDATE''
%2$s  then
    return null;
  end if;
  update %3$s
    set expired_at = coalesce(NEW.changed_at, now())
    where expired_at is null
%4$s      ;
  if TG_OP = ''DELETE'' then
    insert into %3$s(%5$s, changed_at, changed_by)
      values (%6$s, now(), l_user_id);				  
  else
    insert into %3$s(%7$s)
      values(%8$s);
  end if;
  return null;
end 
$body$;
  
create or replace trigger %1$s_after_trigger
  after insert or update or delete
  on %1$s
  for each row
  execute procedure %1$s_after_trigger_fnc();';
begin
  -- Проверяем, существует ли основная таблица
  for l_rec in
  ( select null
      from information_schema.tables t
      where t.table_name = p_table_name
      having count(0) = 0
  ) loop
    raise exception 'Table "%" not found', p_table_name;
  end loop;

  -- Ищем первичный ключ в основной таблице
  select array_agg(c.column_name::text)
    into l_primary_key_list
    from   information_schema.table_constraints tc
      join information_schema.constraint_column_usage as ccu
        using (constraint_schema, constraint_name)
      join information_schema.columns as c on c.table_schema = tc.constraint_schema
        and tc.table_name = c.table_name and ccu.column_name = c.column_name
    where constraint_type = 'PRIMARY KEY'
      and tc.table_name = p_table_name;

  if l_primary_key_list is null then
    raise exception 'Primary key for table "%" not found', p_table_name;
  else
    p_exclude_fields = p_exclude_fields || l_changed_list || l_primary_key_list;
  end if;
  
  -- Проверяем есть ли данные в основной таблице (если есть, то not null не сработает)
  execute format('select 1 from %s limit 1', p_table_name) into l_empty_table;
  
  -- Создаем поля в основной таблице, если их нет
  foreach l_str in array l_changed_list loop
    for l_rec in
    ( select null
        from information_schema.columns c
        where c.table_name = p_table_name
          and c.column_name = l_str
        having count(0) = 0
    ) loop
      if l_str = 'changed_by' then
        execute format('alter table %s add column changed_by bigint %s', p_table_name, case when l_empty_table is null then 'not null' end);
        execute format('create index on %s(changed_by)', p_table_name);
      elsif l_str = 'changed_at' then
        execute format('alter table %s add column changed_at timestamp not null default current_timestamp', p_table_name);
      end if;      
    end loop;
  end loop;
  
  -- Если не существует исторической таблицы, то создаем
  for l_rec in
  ( select null
      from information_schema.tables t
      where t.table_name = l_table_name_history
      having count(0) = 0
  ) loop
    execute format('create table %s as select * from %s where 0 = 1', l_table_name_history, p_table_name);
    execute format('alter table %s add column expired_at timestamp', l_table_name_history);
  end loop;
  
  -- Добавляем и изменяем столбцы, если они есть
  for l_rec in
  ( select t1.column_name
         , case when t1.data_type = 'ARRAY'               then substr(t1.udt_name, 2) || '[]'
                when t1.udt_name in ('varchar', 'varbit') then t1.udt_name || '(' || t1.character_maximum_length || ')'
                when t1.data_type = 'numeric'             then t1.udt_name || case when t1.numeric_precision is not null
                                                                                     then '(' || t1.numeric_precision || ',' || t1.numeric_scale || ')'
                                                                              end
                else t1.data_type
           end as data_type
         , case when t2.column_name is null then 'add'
                when t1.data_type <> t2.data_type
                  or ( coalesce(t1.character_maximum_length, -1) <> coalesce(t2.character_maximum_length, -1)
                    or coalesce(t1.numeric_precision       , -1) <> coalesce(t2.numeric_precision       , -1)
                    or coalesce(t1.numeric_scale           , -1) <> coalesce(t2.numeric_scale           , -1)
                     ) then 'alter column'
           end as mode
      from        information_schema.columns t1
        left join (select t.* from information_schema.columns t where t.table_name = l_table_name_history) t2
          using(column_name)
      where t1.table_name = p_table_name
      order by t1.ordinal_position
  ) loop
    if l_rec.mode is not null then
      if l_rec.mode = 'alter column' then
        l_rec.data_type = 'type '|| l_rec.data_type;
      end if;
      execute format('alter table %s %s %s %s', l_table_name_history, l_rec.mode, l_rec.column_name, l_rec.data_type);
    end if;
  end loop;
  
  -- Создаем индекс по первичному ключу в исторической таблице
  for l_rec in
  ( with indexes as
    ( select i.relname as index_name
           , array_agg(a.attname) as column_names
        from pg_class t
           , pg_class i
           , pg_index ix
           , pg_attribute a
        where t.oid = ix.indrelid
          and i.oid = ix.indexrelid
          and a.attrelid = t.oid
          and a.attnum = ANY(ix.indkey)
          and t.relkind = 'r'
          and t.relname = l_table_name_history
        group by i.relname
        order by i.relname
    )
    select null
      from indexes i
      where i.column_names::text[] = l_primary_key_list
      having count(0) = 0
  ) loop
    execute format('create index on %s(%s)', l_table_name_history, array_to_string(l_primary_key_list, ', '));
  end loop;
 
  -- Подготавливаем данные для формирования триггеров
  foreach l_str in array l_primary_key_list loop
    l_primary_key_where = l_primary_key_where || format('      and %1$s = OLD.%1$s', l_str) || chr(10);
  end loop;
  for l_rec in
  ( select column_name
      from information_schema.columns c
      where c.table_name = p_table_name
        and c.column_name <> all(p_exclude_fields)
        and c.data_type <> all(l_invalid_types)
  ) loop
    l_field_list = l_field_list || l_rec.column_name;
    l_fields_unchanged = l_fields_unchanged || format('    and ((OLD.%1$s = NEW.%1$s) or (OLD.%1$s is null and NEW.%1$s is null))', l_rec.column_name) || chr(10);
  end loop;
  l_field_list = l_primary_key_list || l_field_list;
  -- Создание before-триггера
  execute format(l_before_trigger_pattern, p_table_name, l_fields_unchanged);
  -- Создание after-триггера
  execute format
  ( l_after_trigger_pattern
  , p_table_name
  , l_fields_unchanged
  , l_table_name_history
  , l_primary_key_where
  , array_to_string(l_primary_key_list, ', ')
  , 'OLD.' || array_to_string(l_primary_key_list, ', OLD.')
  , array_to_string(l_field_list, ', ')
  , 'NEW.' || array_to_string(l_field_list, ', NEW.')
  );
end
$create_history$;