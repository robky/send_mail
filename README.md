# Сервис отправки имейл рассылок
### Описание
Возможности сервиса:
 - Отправка рассылок с использованием html макета. Оправка осуществляется по списку подписчиков. 
 - В html макете рассылок можно использовать переменные (имя, фамилия и день рождения подписчика)
 - Отправка отложенных рассылок. Задаются отсрочкой в секундах и/или указанием конкретной даты и времени. 
 - Отслеживание открытий писем (при помощи tracker pixel).
 - Для CRUD операций используется ajax запросы. Формы выводятся в модальном окне. 

Отправка рассылок реализовано в виде задач при помощи Celery.
Проект собирается в Docker контейнерах при помощи docker-compose. 

### Порядок работы
1. Создать пользователей с указанием имя/фамилия/день рождения.
2. Создать рассылку, заполнить html макет.
3. Подписать на рассылку необходимых пользователей.
4. Отправить рассылку, при необходимости указать отсрочку.
5. Результаты отправки смотреть в журнале отправленных рассылок.
6. Если рассылка была отправлена, то можно посмотреть отслеживание открытия писем конкретным пользователем. 
7. При необходимости результаты выполнения задач Celery можно смотреть при помощи Flower.

### Технологии
```
Python 2.7 (Являлось обязательным условием для выполнения данного проекта)
Django 1.11
Gunicorn
PostrgreSQL
Nginx
Redis
Celery
Flower
docker-compose
```

### Подготовка к запуску:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/robky/send_mail.git
cd send_mail
```

### Как запустить рабочий проект:

Переименовать файл .env.example
```
mv .env.example .env
```

Заполнить файлы .env актуальными данными согласно примера.
```text
DEBUG=NO Отключен режим отладки, если указан (DEBUG=YES) выводится отладочная информация
SECRET_KEY Ключ безопастности django
ALLOWED_HOSTS Указывается ip адрес где будет развернут сервис

EMAIL_FILE_BACKEND=NO Если указано YES (EMAIL_FILE_BACKEND=YES) почта фактически не отправляется, а создаются файлами в папке sent_emails worker контейнера.

Следующие значения используются для отправки почты
EMAIL_USE_TLS=YES Использование TLS
EMAIL_HOST Сервер исходящей почты
EMAIL_PORT Порт исходящей почты
EMAIL_HOST_USER Почтовый адрес. Именно с этого почтового адреса происходит отправка рассылок
EMAIL_HOST_PASSWORD Пароль почтового адреса

Следующие значения используются для Redis
REDIS_SERVER=redis Сервер Redis
REDIS_PORT=6379 Порт
REDIS_DB=0 Номер базы данных

Следующие значения используются для Postgres. Если не указана, то по умолчанию используется sqlite.
ENGINE=django.db.backends.postgresql Движок Postgres
POSTGRES_DB Название базы данных
POSTGRES_USER Пользователь
POSTGRES_PASSWORD Пароль пользователя
POSTGRES_SERVER=db Сервер Postgres
POSTGRES_PORT=5432 Порт
```

Запустить контейнер c рабочим проектом
```
docker-compose up -d
```

- Проект будет доступен на 80 порту.
- Flower будет доступен на 9000 порту.

Если отсутствуют статические файлы, то выполнить
```
docker-compose exec web python manage.py collectstatic --no-input
```