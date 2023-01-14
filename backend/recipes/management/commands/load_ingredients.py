import csv
from os import path

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружаем ингридиенты'

    def handle(self, *args, **options):
        filename = path.join('.', 'data', 'ingredients.csv')
        try:
            with open(filename, 'r', encoding='UTF-8') as file:
                data = csv.reader(file)
                for row in data:
                    name, measure = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measure
                    )
            self.stdout.write(self.style.SUCCESS(
                'Все ингридиенты загружены!'
                )
            )
        except FileNotFoundError as error:
            raise CommandError(error)
