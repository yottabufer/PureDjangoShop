from django.urls import path
from .views import AllProductView, DetailProduct, CreateProductView, BasketView

urlpatterns = [
    path('', AllProductView.as_view(), name='all_product'),
    path('product/create', CreateProductView.as_view(), name='create_product'),
    path('product/<int:pk>', DetailProduct.as_view(), name='detail_product'),
    path('basket', BasketView.as_view(), name='basket'),

]
