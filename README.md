### Foodgram
## Описание проекта 
 
Foodgram это сервис для публикации рецептов блюд. 
 
Ресурс позволяет публиковать собственные рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а также скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
 
## Установка и запуск проекта локально

Для того, чтобы запустить сервис локально на своем компьютере, нужно выполнить следующие шаги:

1. Клонировать репозиторий на компьютер:
```
git clone https://github.com/vavilovnv/foodgram-project-react.git
```

2. Перейти в директорию проекта:
```
cd foodgram-project-react
```

3. Cоздать и активировать виртуальное окружение:

```
python -m venv venv

# linux
source venv/bin/activate

# windows
source venv/source/activate
```

4. Перейти в директорию `/infra` и создать файл `.env`:

```
cd infra
touch .env
```

5. Заполнить файл следующим содержанием:
```
SECRET_KEY=секретная комбинация из одноименного параметра в settings.py
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

6. Перейти в директорию `/backend` и установить зависимости из файла requirements.txt:

```
cd ..
cd backend
pip install -r requirements.txt
```

7. Сформировать и выполнить миграции:

```
python manage.py makemigrations

# в случае, если файлы миграций не формируются командой выше, запустить команду
# последовательно с указанием имен приложений users и recipes в следующем формате
python manage.py makemigrations [имя приложения]

python manage.py migrate
```

8. Создать супер-пользователя:
```
python manage.py createsuperuser
```

9. Импортировать ингредиенты:
```
python manage.py import_ingredients
```

10. Собрать статику:
```
python manage.py collectstatic
```

11. Запустить dev-сервер:
```
python manage.py runserver
```

12. Перейти в директорию `/frontend`:
```
cd ..
cd frontend
```

13. Изменить адрес в файле `package.json` заменив строку `"proxy": "http://web:8000/"` на `"proxy": "http://127.0.0.1:8000/"`.

14. Установить Node.js и npm. Пример установки на Ubuntu можно найти [здесь](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04).

15. Запустить фронт:
```
npm install --legacy-peer-deps
npm run build
npm start
```


## Запуск проекта в Docker

Для запуска проекта в docker, нужно выполнить следующие шаги:

1. Установить Docker и Docker-compose. Пример установки на Ubuntu можно посмотреть [здесь](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru).

Параметры описаны в конфигах `docker-compose.yml` и `nginx.conf` в директории `infra/`. При необходимости нужно добавить или изменить адреса проекта в файле `nginx.conf`

2. Запустить docker compose:
```
sudo docker-compose up -d --build
```
  
  После сборки создадутся три контейнера:
  > 1. контейнер базы данных `db`
  > 2. контейнер приложения `backend`
  > 3. контейнер web-сервера `nginx`

3. Создать миграции
```
sudo docker-compose exec backend python manage.py makemigrations

# в случае, если файлы миграций не формируются командой выше, запустить команду
# последовательно с указанием имен приложений users и recipes в следующем формате
sudo docker-compose exec backend python manage.py makemigrations [имя приложения]
```

4. Применить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```

8. Создать супер-пользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```

9. Импортировать ингредиенты:
```
sudo docker-compose exec backend python manage.py import_ingredients
```

10. Собрать статику:
```
sudo docker-compose exec backend python manage.py collectstatic
```


## Сайт проекта
Сайт проекта доступен по адресу: [http://foodgrams.ddns.net](http://foodgrams.ddns.net)(если сервер не потушен).


## Технологическй стек

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Проект в интернете
Проект запущен и доступен по [адресу](http://84.252.142.130//recipes)
Админка доступна по почте\паролю: SuperAdmin@gmail.com \ SuperAdmin@gmail.com
