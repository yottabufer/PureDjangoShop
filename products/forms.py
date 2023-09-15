from django.forms import ModelForm
from .models import ProductModel


class CreateProductForm(ModelForm):
    class Meta:
        model = ProductModel
        fields = ('title', 'description', 'price', 'specifications', 'shop', 'quantity_product_in_shop')
