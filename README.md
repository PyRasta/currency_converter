### Описание
Код в фоне берет курс валют из <a href='https://currencylayer.com'>currencylayer.com</a> и записывает(обновляет)
в базу данных с интервалом, который установлен в переменной `TIME_UPDATE_RATES_SEC`.
Добавлен интервал, так как сервис предоставляет 1000 запросов в месяц,
делая 24 запроса в сутки, нам хватит этих запросов. Для работы  так же требуется `ACCESS KEY`, я его вам оставил для проверки кода.
В fastapi есть встроенный swagger - http://127.0.0.1:8000/docs


### Настройка
Отредактируйте файл `.env`, а именно переменную `TIME_UPDATE_RATES_SEC`, это частота обновления курса валют в секундах

### Запуск
Сборка образов
```
$ docker-compose build
```
Запуск контейнеров
```
$ docker-compose up -d
```
Просмотр логов
```
$ docker-compose logs
```
### P.S
В этом тестовом задании я хотел показать почти все мои умения, от проектирования проекта, до ассихронности, celery, docker, использование бд и т.д.
Рассчитываю, что после этого тестового задания я попаду на собеседования, буду рад с вами пообщаться.
Мой телеграм: @rasta_qq

