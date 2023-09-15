from django.db import models
from django.urls import reverse


class ShopForProduct(models.Model):
    title = models.CharField(max_length=70, verbose_name='title')
    description = models.TextField(max_length=255, verbose_name='description')
    objects = models.Manager()

    def __str__(self):
        return self.title


class ProductModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    description = models.TextField(max_length=255, verbose_name='description')
    price = models.IntegerField(default=0, editable=True, verbose_name='price')
    specifications = models.TextField(max_length=500, verbose_name='specifications')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    shop = models.ManyToManyField('ShopForProduct', verbose_name='shop', null=True)
    quantity_product_in_shop = models.PositiveIntegerField(default=1, verbose_name='quantity products', null=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_product', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at', 'title']
