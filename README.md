Проект api_yamdb предоставляет возможность взаимодействия приложений с сервисом yamdb, позволяющим выставлять оценки и писать отзывы на различные произведения. В данном проекте реализована концепция CRUD по отношению к произведениям, пользователям, категориям, жанрам, отзывам и комментариям. Подробности описаны в технической документации проекта.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:cosmofactory/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Документация проекта находится по адресу (при запуске на локальном сервере):

```
http://127.0.0.1:8000/redoc/
```

Примеры некоторых запросов-ответов к API:

```
GET http://127.0.0.1:8000/api/v1/titles/
```

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```


```
POST http://127.0.0.1:8000/api/v1/titles/
```

```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```


Авторы: 
Екатерина Хиталенко (krchkv94@yandex.ru)
Дмитрий Киткин (Dimas-0007@yandex.ru)
Никита Ассоров (nikssor@yandex.ru)

```
https://github.com/cosmofactory
```
Используемые технологии: DRF, JWT, REST API, Redoc