from abc import ABC
from django.core.management import BaseCommand
from ...models import ShopForProduct
from django.utils.crypto import get_random_string


class Command(BaseCommand, ABC):
    def handle(self, *args, **options):
        self.stdout.write('Создание магазинов')
        for new_shop in range(5):
            shop, created = ShopForProduct.objects.get_or_create(
                title=get_random_string(10),
                description=get_random_string(250),
            )
            self.stdout.write(f'Создал {shop.title}')

        self.stdout.write(self.style.SUCCESS('Успешно'))
