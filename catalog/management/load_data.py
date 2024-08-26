from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json

class Command(BaseCommand):
    help = 'Load data from fixtures into the database'

    @staticmethod
    def json_read(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def handle(self, *args, **options):
        # Удалите все объекты из базы данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузите категории и продукты из фикстур
        categories_data = self.json_read('catalog/fixtures/categories_data.json')
        products_data = self.json_read('catalog/fixtures/products_data.json')

        # Создайте объекты Category
        categories_for_create = []
        for category in categories_data:
            categories_for_create.append(
                Category(
                    id=category['pk'],
                    name=category['fields']['name'],
                    description=category['fields']['description']
                )
            )
        Category.objects.bulk_create(categories_for_create)

        # Создайте объекты Product
        products_for_create = []
        for product in products_data:
            category = Category.objects.get(id=product['fields']['category'])
            products_for_create.append(
                Product(
                    id=product['pk'],
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    image=product['fields']['image'],
                    category=category,
                    price=product['fields']['price'],
                    manufactured_at=product['fields']['manufactured_at']
                )
            )
        Product.objects.bulk_create(products_for_create)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
