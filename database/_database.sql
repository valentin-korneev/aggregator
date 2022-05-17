do
$$
begin
  if not exists ( select from pg_database where datname = 'aggregator' ) then
    create database aggregator with
      owner = aggregator
      encoding = 'UTF8'
      connection limit -1;
  end if;
end
$$;