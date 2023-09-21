import random
from abc import ABC
from django.core.management import BaseCommand
from ...models import ShopForProduct
from ...models import ProductModel
from django.utils.crypto import get_random_string


class Command(BaseCommand, ABC):
    def handle(self, *args, **options):
        self.stdout.write('Создание товара')
        for _ in range(250):
            product, created = ProductModel.objects.get_or_create(
                title=get_random_string(10),
                description=get_random_string(10),
                price=random.randint(10, 1000),
                specifications=get_random_string(10),
                quantity_product_in_shop=random.randint(10, 100),
                shop=ShopForProduct.objects.get(pk=random.randint(1, 5))

            )

            # product.shop.set(shop)  # Создание ManyToMany
            product.save()
            self.stdout.write(f'Создал {product.title}')

        self.stdout.write(self.style.SUCCESS('Успешно'))
