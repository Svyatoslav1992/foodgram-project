from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создаем пользователей'

    def handle(self, *args, **kwargs):
        data = [
            {'username': 'Ivan', 'first_name': 'Ivan', 'last_name': 'Ivan',
                'email': 'Ivan@gmail.com', 'password': '1q2w3e4r'},
            {'username': 'Slava', 'first_name': 'Слава', 'last_name': 'Килин',
                'email': 'Svyatoslav@gmail.com', 'password': '1q2w3e4r'},
            {'username': 'Darya', 'first_name': 'Дарья', 'last_name': 'Ан',
                'email': 'Darya@gmail.com', 'password': '1q2w3e4r'},
        ]
        User.objects.bulk_create(User(**user) for user in data)
        self.stdout.write(self.style.SUCCESS('Все пользователи созданы!'))
