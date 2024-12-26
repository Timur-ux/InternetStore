-- Удаляем все таблицы в базе данных internetstore

-- Сначала удаляем промежуточную таблицу item_shop
DROP TABLE IF EXISTS item_shop CASCADE;

-- Затем удаляем таблицы, которые ссылаются на другие таблицы
DROP TABLE IF EXISTS user_actions CASCADE;
DROP TABLE IF EXISTS buy CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Удаляем таблицы, которые не имеют внешних ключей
DROP TABLE IF EXISTS action CASCADE;
DROP TABLE IF EXISTS access CASCADE;
DROP TABLE IF EXISTS item_category CASCADE;

-- Наконец, удаляем таблицы item и shop
DROP TABLE IF EXISTS item CASCADE;
DROP TABLE IF EXISTS shop CASCADE;
