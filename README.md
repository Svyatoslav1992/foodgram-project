### Foodgram

```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker-compose exec web python manage.py load_ingredients
sudo docker-compose exec web python manage.py load_tags

sudo docker-compose exec web python manage.py createsuperuser
```