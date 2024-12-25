-- Заполнение таблицы access
INSERT INTO access(name)
VALUES
  ('user'),
  ('administrator');

-- Заполнение таблицы action
INSERT INTO action(name)
VALUES
  ('buy');

-- Заполнение таблицы users
INSERT INTO users(access_level, login, password)
VALUES
  ((SELECT id FROM access WHERE name = 'administrator'), 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');

-- Заполнение таблицы shop
INSERT INTO shop(shop_name)
VALUES
  ('Shop A'),
  ('Shop B'),
  ('Shop C');

-- Заполнение таблицы item_category
INSERT INTO item_category(item_category_name)
VALUES
  ('Electronics'),
  ('Clothing'),
  ('Home Appliances');

-- Заполнение таблицы item
INSERT INTO item(item_id, item_name, uri, item_category_id, item_price, item_cnt_day, date, date_block_num, shop_id, shop_name, item_category_name)
VALUES
  (1, 'Smartphone', 'http://example.com/item/1', 1, 699.99, 10, '2023-10-01', 33, 1, 'Shop A', 'Electronics'),
  (2, 'Laptop', 'http://example.com/item/2', 1, 1299.99, 5, '2023-10-01', 33, 2, 'Shop B', 'Electronics'),
  (3, 'T-Shirt', 'http://example.com/item/3', 2, 19.99, 20, '2023-10-01', 33, 1, 'Shop A', 'Clothing'),
  (4, 'Washing Machine', 'http://example.com/item/4', 3, 499.99, 2, '2023-10-01', 33, 3, 'Shop C', 'Home Appliances'),
  (5, 'Headphones', 'http://example.com/item/5', 1, 89.99, 15, '2023-10-01', 33, 2, 'Shop B', 'Electronics');
