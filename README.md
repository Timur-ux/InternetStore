# Интернет магазин
Работа по курсу IT-проекты 5го семестра

## Структура
3х элементная структура: фронт, бэк и база данных

### backend
Тут обычный сервер на fastapi с возможностью авторизации, получения данных

### backend: TODO
  - [x] Управление пользователями: авторизация и регистрация(с сохранением токена в куках браузера)
  #### Со стороны пользователя:
  - [x] 1. Получение списка всех товаров(Товар содержит следующие поля: имя, uri(url запрос для получения данных об этом товаре), id товара,  список id магазинов где он продается, список цен для каждого магазина[Вся эта инфа лежит в датасете для ml модели, можешь(т.е. по желанию) сделать структуру таблицы, как и в датасете]).
  - [x] 2. Получение данных о списке товаров(передается список uri к ним или список id(сделай как сам считаешь будет лучше))
  - [x] 3. Получение данных о балансе пользователя и его пополнение(если не выйдет сделать оплату через сторонний сервис)
  - [x] 4. Покупка товаров(прилетает список из id или uri, решай сам)
  #### Со стороны администратора:
  - [x] 1. Получение прогноза продаж для списка товаров(товары прилетают в виде uri или id). Если списка нет -- нужен прогноз для всех товаров. Сервис для прогнозирования я опишу сам тебе надо будет только сделать запрос на адрес сервиса. Также укажи pydantic модель, в которой будешь хранить тело запроса.
  - [x] В дополнение после авторизации в ответе присылай тип авторизированного пользователя(рядовой пользователь/администратор), т.к. они будут входить в аккаунт через одну форму 

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
