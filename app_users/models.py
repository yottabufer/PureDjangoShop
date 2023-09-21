from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from products.models import ProductModel
import logging
from django.db.models import Sum, F

logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    class StatusUser(models.TextChoices):
        bronze = 'bronze'
        silver = 'silver'
        gold = 'gold'

    username = models.CharField(max_length=255, unique=True, verbose_name='Username')
    USERNAME_FIELD = 'username'
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    balance_user = models.IntegerField(default=0, help_text='User balance', verbose_name='User balance')
    total_expenses = models.IntegerField(default=0, editable=True, verbose_name='Total user expenses')
    status = models.CharField(max_length=255, choices=StatusUser.choices, default=StatusUser.bronze,
                              verbose_name='user status')
    # user_basket = models.ForeignKey('Basket', on_delete=models.CASCADE, verbose_name='basket', null=True)
    user_order_history = models.ForeignKey('UsersOrderHistory', on_delete=models.CASCADE, verbose_name='order history',
                                           null=True)

    @staticmethod
    def get_order_history():
        return UsersOrderHistory.test_func()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id', 'last_name']

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def update_status_user(self):
        if 50_000 <= self.total_expenses <= 100_000:
            self.status = self.StatusUser.silver
            self.save()
        elif self.total_expenses > 100_000:
            self.status = self.StatusUser.gold
            self.save()
        logger.debug("test message in transition by status system")
        return self.status


class PartBasket(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='product', null=True)
    quantity_product = models.PositiveIntegerField(default=1, verbose_name='quantity products', null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.product)

    def get_absolute_url(self):
        return reverse('detail_product', kwargs={'pk': self.product.pk})


class Basket(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='user')
    part_basket = models.ManyToManyField(PartBasket, verbose_name='product')
    objects = models.Manager()

    def get_total_cost(self):
        queryset = PartBasket.objects.filter(basket=self.pk).aggregate(total_cost=Sum(F('product__price') * F('quantity_product')))["total_cost"]
        return queryset


class PartUsersOrderHistory(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='product', null=True)
    quantity_product = models.PositiveIntegerField(default=1, verbose_name='quantity products', null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.product)

    def get_absolute_url(self):
        return reverse('detail_product', kwargs={'pk': self.product.pk})


class UsersOrderHistory(models.Model):
    part_users_order = models.ManyToManyField(PartUsersOrderHistory, verbose_name='product')

    @staticmethod
    def test_func():
        return PartUsersOrderHistory.objects.all()
