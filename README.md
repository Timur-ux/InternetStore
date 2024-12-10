# Интернет магазин
Работа по курсу IT-проекты 5го семестра

## Структура
3х элементная структура: фронт, бэк и база данных

### backend
Тут обычный сервер на fastapi с возможностью авторизации, получения данных

## Запросы в curl для проверки работы api

* регистрация пользователя
```bash
curl -X POST -H "Content-Type: application/json" -d '{"login": "your_login", "password": "your_password", "access_level": "1"}' http://localhost:5000/api/register
```

### backend: TODO
  1. Сделать систему авторизации (банальная передача логина и пароля с занесением в базу данных)
  2. Сделать обработку основных запросов(получения списка товаров, получение какого-то конкретного товара и т.д.)
  3. Обернуть все это дело в шифрованное соединение. Завернуть все в какое-нибудь SHA-256 шифрование и проверку личности через jwt токены

### frontend
  Фронт написан на react js с библиотекой axios для создания запросов

### frontend: TODO
  1. Сделать форму входа
  2. Сделать форму регистрации
  3. Сделать форму списка товаров
  4. Сделать форму информации о товаре
  5. Сделать форму корзины
  6. Обернуть все запросы в шифрованное соединение. Завернуть все в какое-нибудь SHA-256 шифрование и проверку личности через jwt токены

# Команда Боевые пчелки
- Тимур
- Андрей
- Михаил
- Мирон

    Потом напишу полные ФИО
