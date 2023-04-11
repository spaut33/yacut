# YACUT - Yet Another Custom URL Tool (Сервис сокращения ссылок)

## Описание

`YACUT` - новое слово в сокращении ссылок, сервис, позволяющий гененрировать
короткие ссылки на любые ресурсы в интернете. YACUT создает
короткие ссылки через удобную форму на сайте, а также через API.

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```shell
git clone git@github.com:spaut33/yacut.git
```

```shell
cd yacut
```

Cоздать и активировать виртуальное окружение:

```shell
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```shell
    source venv/bin/activate
    ```

* Если у вас windows

    ```shell
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```shell
python3 -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

## Запуск

Перед самым первым запуском необходимо создать базу данных, для этого в командной
строке нужно выполнить:
```shell
flask db upgrade
```
Приложение запускается командой:
```shell
flask run
```
При запуске приложения в консоли будет выведен адрес, по которому можно будет
перейти на сайт сервиса. По умолчанию это `http://127.0.0.1:5000/`.
После запуска на странице главной странице сервиса будет создана форма для 
генерации коротких ссылок, а также будет доступен API для работы с сервисом.

## Примеры использования API:

### Создание короткой ссылки - `POST /api/id/`
Параметр `custom_id` - опциональный, если он не указан, то сервис сгенерирует
сокращение для ссылки самостоятельно. Если данный параметр указан, то сервис проверит, что такого сокращения
еще нет в базе данных, иначе будет возвращена ошибка 400.
```json
{
  "url": "http://ya.ru",
  "custom_id": "ya"
}
```

### Получение информации о ссылке - `GET /api/id/{custom_id}`
В запросе вместо `custom_id` нужно подставить сокращение ссылки, если такое сокращение 
существует, то в ответе будет информация о ссылке, если такого сокращения нет, то будет возвращена ошибка 404.
Пример ответа API, если сокращение было найдено:
```json
{
  "url": "http://ya.ru"
}
```

## Технологии

* [Python 3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [WTForms](https://wtforms.readthedocs.io/en/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/)


## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)

## Автор

[Roman Petrakov](https://github.com/spaut33/)