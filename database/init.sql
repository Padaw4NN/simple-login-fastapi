do $$
begin
    if not exists (select from pg_database where datname = 'credentials') then
        create database credentials;
    end if;
end $$;

create table if not exists users (
    id       serial       not null primary key,
    username varchar(32)  not null unique,
    password varchar(128) not null,
    email    varchar(128) not null unique
);
