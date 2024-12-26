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
  ((SELECT id FROM access WHERE name = 'administrator'), 'admin', '$2a$10$YgzepzPAE0OZWr9P6mQVu.Ind9xcSN/DGCfOiVT8XClxWjWLWbfpa');

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
INSERT INTO item(item_id, item_name, uri, item_category_id, item_price, item_cnt_day, date, date_block_num, item_category_name)
VALUES
  (1, 'Smartphone', 'http://example.com/item/1', 1, 699.99, 10, '2023-10-01', 33, 'Electronics'),
  (2, 'Laptop', 'http://example.com/item/2', 1, 1299.99, 5, '2023-10-01', 33, 'Electronics'),
  (3, 'T-Shirt', 'http://example.com/item/3', 2, 19.99, 20, '2023-10-01', 33, 'Clothing'),
  (4, 'Washing Machine', 'http://example.com/item/4', 3, 499.99, 2, '2023-10-01', 33, 'Home Appliances'),
  (5, 'Headphones', 'http://example.com/item/5', 1, 89.99, 15, '2023-10-01', 33, 'Electronics');

-- Связывание товаров с магазинами в промежуточной таблице item_shop
INSERT INTO item_shop(item_id, shop_id)
VALUES
  (1, 1),  -- Smartphone в Shop A
  (1, 2),  -- Smartphone в Shop B
  (2, 2),  -- Laptop в Shop B
  (3, 1),  -- T-Shirt в Shop A
  (4, 3),  -- Washing Machine в Shop C
  (5, 2);  -- Headphones в Shop B
