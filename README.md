### Foodgram
### Описание
Приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.А перед походом в магазин можно скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Технологии
- Python 3.7
- Django 3.2.16
- Django Rest Framework 3.12.14
- Docker 20.10.18
- Djoser==2.1.0
- Yandex Cloud
- Postgres


### Особенности
- применены вьюсеты;
- для аутентификации использованы возможности библиотека djoser;
- у неаутентифицированных пользователей доступ к API только на чтение;
- для загрузки проекта применен Docker, подготовлены файлы для развертывания инфраструктуры;
- настроены Continuous Integration и Continuous Deployment;

### Установка
- склонировать репозиторий
```sh
git clone github.com/Svyatoslav1992/foodgram-project-react.git
```
- в директории foodgram-project-react/infra/ создаем файл .env и записываем в него следующие переменные окружения:
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=<имя базы данных>
  POSTGRES_USER=<ваш_логин для подключения к базе данных>
  POSTGRES_PASSWORD=<ваш_пароль для подключения к базе данных>
  DB_HOST=<название сервиса(контейнера)>
  DB_PORT=<порт для подключения к базе данных>
  ALLOWED_HOSTS=<список хостов, доступных сайту>

- в директории foodgram-project-react/infra/ выполняем команду для сбори контейнеров
```sh
docker-compose up -d --build
```

- внутри собранных котейнеров создаем и выполняем миграции, создаем суперпользователя и собираем статику
```sh
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py load_data
```

- проект доступен по адресу http://<IP вашей машины>/

### Примеры запросов
  - POST   http://localhost/api/recipes/

    {
        "ingredients": [
        {
        "id": 1123,    "amount": 10}
        ],
        "tags": [
        1,
        2
        ],
        "image": "data:image/png;base64,iVBORw0KG...",
        "name": "string",
        "text": "string",
        "cooking_time": 1}

  - DELETE http://localhost/api/recipes/{id}/

  - GET http://localhost/api/ingredients/
    [
    {
        "id": 0,
        "name": "Капуста",
        "measurement_unit": "кг"
     }
     ]

  - GET   http://localhost/api/tags/

    [
        {
        "id": 0,
        "name": "Завтрак",
        "color": "#E26C2D",
        "slug": "breakfast"
        }
]

