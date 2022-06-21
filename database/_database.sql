do
$$
begin
  if not exists ( select from pg_database where datname = 'aggregator' ) then
    create extension if not exists dblink;
    perform dblink_exec(''
    ,  'create database aggregator with
          owner = aggregator
          encoding = ''UTF8''
          connection limit -1'
    );
  end if;
end
$$;