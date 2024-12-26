create database internetstore;

\c internetstore

-- Обновление таблицы item (удаление shop_id)
CREATE TABLE item (
  item_id BIGSERIAL PRIMARY KEY,                       -- Уникальный идентификатор товара
  item_name VARCHAR(100) NOT NULL,                -- Название товара
  uri VARCHAR(255) NOT NULL,                      -- URL для получения данных о товаре
  item_category_id BIGINT NOT NULL,               -- Уникальный идентификатор категории товара
  item_price NUMERIC(10, 2) NOT NULL,            -- Текущая цена товара
  item_cnt_day INT,                               -- Количество проданных товаров за день
  date DATE,                                       -- Дата в формате dd/mm/yyyy
  date_block_num INT,                             -- Номер месяца (0 - январь 2013, 1 - февраль 2013 и т.д.)
  item_category_name VARCHAR(100) NOT NULL        -- Название категории товара
);

-- Обновление таблицы shop (остается без изменений)
CREATE TABLE shop (
  shop_id BIGSERIAL PRIMARY KEY,                  -- Уникальный идентификатор магазина
  shop_name VARCHAR(100) NOT NULL                 -- Название магазина
);

-- Создание промежуточной таблицы для связи многие-ко-многим
CREATE TABLE item_shop (
  item_id BIGINT NOT NULL,                       -- Уникальный идентификатор товара
  shop_id BIGINT NOT NULL,                       -- Уникальный идентификатор магазина
  PRIMARY KEY (item_id, shop_id),                -- Композитный первичный ключ
  FOREIGN KEY (item_id) REFERENCES item(item_id),     -- Внешний ключ на таблицу item
  FOREIGN KEY (shop_id) REFERENCES shop(shop_id) -- Внешний ключ на таблицу shop
);

CREATE TABLE item_category (
  item_category_id BIGSERIAL PRIMARY KEY,       -- Уникальный идентификатор категории товара
  item_category_name VARCHAR(100) NOT NULL       -- Название категории товара
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
  item_id bigint not null,
  price NUMERIC(10, 2),
  cnt INT,
  buy_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
  id bigserial PRIMARY KEY,
  access_level bigint NOT NULL,
  login varchar(100),
  password varchar(64),
  balance decimal(10, 2) DEFAULT 0.00
);

create table  access (
  id bigserial primary key,
  name varchar(100)
);
create table  action (
  id bigserial primary key,
  name varchar(100)
);