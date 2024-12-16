create database InternetStore;

\c InternetStore

create table  item (
  id bigserial primary key,
  name varchar(100),
  uri BIGINT not NULL,
  description TEXT,
  price NUMERIC(10, 2),
  stock INT
);

create table  user_actions (
  id bigserial primary key,
  user_id bigint not null,
  action varchar(100) not null
);

create table  users (
  id bigserial primary key,
  access_level bigint not null,
  login varchar(100),
  password varchar(64)
);

create table  access (
  id bigserial primary key,
  name varchar(100)
);