-- Очищаем все таблицы в базе данных internetstore

-- Сначала очищаем промежуточную таблицу item_shop
TRUNCATE TABLE item_shop CASCADE;

-- Затем очищаем таблицы, которые ссылаются на другие таблицы
TRUNCATE TABLE user_actions CASCADE;
TRUNCATE TABLE buy CASCADE;
TRUNCATE TABLE users CASCADE;

-- Очищаем таблицы, которые не имеют внешних ключей
TRUNCATE TABLE action CASCADE;
TRUNCATE TABLE access CASCADE;
TRUNCATE TABLE item_category CASCADE;

-- Наконец, очищаем таблицы item и shop
TRUNCATE TABLE item CASCADE;
TRUNCATE TABLE shop CASCADE;
