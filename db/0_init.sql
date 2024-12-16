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

CREATE TABLE user_actions (
  id bigserial PRIMARY KEY,
  user_id bigint NOT NULL,
  action varchar(100) NOT NULL,
  action_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table  buy (
  id bigserial primary key,
  user_id bigint not null,
  price NUMERIC(10, 2),
  cnt INT,
  buy_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
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
create table  action (
  id bigserial primary key,
  name varchar(100)
);