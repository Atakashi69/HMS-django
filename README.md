# Веб-приложение для управления отелем на django

## Запуск приложения
1. Установите Python: Убедитесь, что на компьютере установлен Python. Вы можете загрузить и установить его с официального сайта Python (https://www.python.org).
2. Установите зависимости проекта: Перейдите в корневую папку вашего проекта Django, где находится файл requirements.txt. Откройте командную строку (или терминал) и выполните следующую команду:
`pip install -r requirements.txt`
Это установит все зависимости проекта, необходимые для его работы.

3. Настройте базу данных: Если ваше приложение использует базу данных, убедитесь, что у вас есть доступ к базе данных и настройки подключения в файле settings.py вашего проекта.

4. Выполните миграции: В командной строке (или терминале) перейдите в корневую папку вашего проекта Django и выполните следующую команду:
`python manage.py migrate`
Это выполнит все необходимые миграции базы данных.

5. Запустите сервер разработки: В командной строке (или терминале) перейдите в корневую папку вашего проекта Django и выполните следующую команду:
`python manage.py runserver`
Это запустит сервер разработки Django, который будет слушать на локальном хосте (обычно http://127.0.0.1:8000/).

6. Откройте веб-браузер: Откройте веб-браузер на вашем компьютере и перейдите по адресу http://127.0.0.1:8000/ (или другому адресу, который указан в выводе команды runserver).

## Документация к API

### Получение списка комнат
### Запрос

`GET /api/rooms/`

### Параметры запроса

- `number` (необязательный): Фильтр по номеру комнаты.
- `capacity` (необязательный): Фильтр по вместимости комнаты.

### Ответ

Статус код: 200 OK

```json
[
  {
    "id": 1,
    "number": "101",
    "price": "2500.00",
    "capacity": 1
  },
  {
    "id": 2,
    "number": "102",
    "price": "2500.00",
    "capacity": 1
  }
]
```

### Создание новой комнаты
### Запрос

`POST /api/rooms/`

### Тело запроса
```json
{
  "number": "110",
  "price": "5000.00",
  "capacity": 2
}
```

### Ответ

Статус код: 201 Created

```json
{
  "id": 10,
  "number": "110",
  "price": "5000.00",
  "capacity": 2
}
```
