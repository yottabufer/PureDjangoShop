import time

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
import logging
from .forms import CreateProductForm
from .models import ProductModel, ShopForProduct
from app_users.models import Basket, PartBasket, PartUsersOrderHistory

logger = logging.getLogger(__name__)


class AllProductView(ListView):
    model = ProductModel
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return ProductModel.objects.prefetch_related('shop').filter(quantity_product_in_shop__gte=1)


class DetailProduct(DetailView):
    model = ProductModel
    context_object_name = 'product'
    template_name = 'products/detail_product.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            basket, created = Basket.objects.get_or_create(user=self.request.user)
            part_basket, created = PartBasket.objects.get_or_create(
                product=self.get_object(),
                quantity_product=request.POST.get('quantity_product'),
                basket=basket)
            part_basket.save()

            return redirect('basket')
        else:
            return redirect('registration')


class CreateProductView(CreateView):
    template_name = 'products/create_product.html'
    form_class = CreateProductForm
    success_url = _('all_product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = ShopForProduct.objects.all()

        return context


class BasketView(ListView):
    model = Basket
    template_name = 'products/basket_user.html'
    context_object_name = 'basket'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            basket_instance, created = Basket.objects.get_or_create(user=self.request.user)
            context['basket'] = basket_instance
            context['part_basket'] = PartBasket.objects.filter(basket=context['basket'])
            context['total_cost_basket'] = context['basket'].get_total_cost()
            return context

    def post(self, request, *args, **kwargs):
        basket_instance, created = Basket.objects.get_or_create(user=self.request.user)
        if request.user.balance_user < basket_instance.get_total_cost():
            logger.debug(f"{request.user.id} -- Мало денег -- {request.user.balance_user} < {basket_instance.get_total_cost()}")
            time.sleep(3)
            return redirect('basket')
        else:
            part_order_history = PartUsersOrderHistory()
            whole_basket = basket_instance.basket.all()
            for one_product in whole_basket:
                one_product.product.quantity_product_in_shop -= int(one_product.quantity_product)
                one_product.product.save()
                part_order_history.product = one_product.product
                part_order_history.quantity_product = one_product.quantity_product
            part_order_history.save()

            request.user.total_expenses += basket_instance.get_total_cost()
            request.user.balance_user -= basket_instance.get_total_cost()
            request.user.update_status_user()
            whole_basket.delete()
            request.user.save()
            logger.debug("test message in making an order and clearing the basket")
            return HttpResponseRedirect(_('all_product'))
