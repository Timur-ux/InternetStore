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
* вход пользователя
```bash
curl -X POST -H "Content-Type: application/json" -d '{"login": "your_login", "password": "your_password"}' http://localhost:5000/api/login
```

* список марок
```bash
curl -X GET http://localhost:5000/api/marks
```

* добавить марку
```bash
curl -X PUT -H "Content-Type: application/json" -d '{ 
  "mark_id": 2,    
  "mark_type": 100,
  "location_id": 1,
  "last_position": [10.5, 20.3, 30.7]
}' http://localhost:5000/api/marks/1
```
* удалить марку
```bash
curl -X DELETE http://localhost:5000/api/marks/1
```

* обновить марку (пока что не работает)
```bash
curl -X POST -H "Content-Type: application/json" -d '{   
  "mark_id": 1,
  "mark_type": 200,
  "location_id": 2,
  "last_position": [15.0, 25.3, 35.7]
}' http://localhost:5000/api/marks/1
```

* запрос на создание администратора 
```bash
curl -X POST \                         
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzQzNzI4MzN9.tU12RnzU0WjiHPvuaHeaYl732OjaNzWlgnCky_kGNOw" \
-d '{"login": "your_login", "password": "your_password", "access_level": "2"}' \
http://localhost:5000/api/register
```


### backend: TODO
  - [x] Сделать систему авторизации (банальная передача логина и пароля с занесением в базу данных)
  - [x] Сделать обработку основных запросов(получения списка товаров, получение какого-то конкретного товара и т.д.)
  - [x] Обернуть все это дело в шифрованное соединение. Завернуть все в какое-нибудь SHA-256 шифрование и проверку личности через jwt токены

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
