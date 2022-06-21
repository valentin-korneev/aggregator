do
$$
begin
  if not exists ( select from pg_roles where rolname = 'aggregator' ) then
    create role aggregator with
      login
      superuser
      nocreatedb
      createrole
      noinherit
      noreplication
      connection limit -1
      password 'admin';
  end if;
end
$$;