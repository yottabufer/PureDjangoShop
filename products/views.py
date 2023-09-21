from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
import logging
from .forms import CreateProductForm
from .models import ProductModel, ShopForProduct
from app_users.models import Basket, PartBasket, CustomUser, PartUsersOrderHistory, UsersOrderHistory
from django.urls import reverse_lazy

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


class CreateProductView(CreateView):
    template_name = 'products/create_product.html'
    form_class = CreateProductForm
    success_url = _('all_product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = ShopForProduct.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        need_product = self.get_object()
        basket, created = Basket.objects.get_or_create(user=request.user)
        basket.product.add(need_product)
        return HttpResponseRedirect(reverse_lazy('detail_product', args=[str(self.object.pk)]))

# def saveorder(request):
#     if request.user.is_authenticated:
#         need_part_basket = PartBasket()
#         need_part_basket.product = ProductModel.objects.get(pk=request.POST['product_pk'])
#         product_in_order = ProductModel.objects.get(pk=request.POST['product_pk'])
#         need_part_basket.quantity_product = request.POST['quantity_product']
#
#         if int(need_part_basket.quantity_product) > int(product_in_order.quantity_product_in_shop):
#             return HttpResponseRedirect(_('all_product'))
#         else:
#             need_part_basket.save()
#             basket_for_user = Basket.objects.get_or_create(user=self.request.user)
#             basket_for_user.save()
#             basket_for_user.part_basket.add(need_part_basket)
#             return redirect('all_product')
#     else:
#         return redirect('registration')


class BasketView(ListView):
    model = Basket
    template_name = 'products/basket_user.html'
    context_object_name = 'basket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_instance, created = Basket.objects.get_or_create(user=self.request.user)
        context['basket'] = basket_instance
        context['total_cost_basket'] = context['basket'].get_total_cost()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.balance_user < self.total_cost_basket():
            return redirect('basket')
        else:
            part_order_history = PartUsersOrderHistory()

            whole_basket = self.request.user.user_basket.part_basket.all()
            for one_product in whole_basket:
                one_product.product.quantity_product_in_shop -= int(one_product.quantity_product)
                one_product.product.save()

                part_order_history.product = one_product.product
                part_order_history.quantity_product = one_product.quantity_product

            part_order_history.save()
            request.user.total_expenses += self.total_cost_basket()
            request.user.balance_user -= self.total_cost_basket()
            request.user.update_status_user()
            whole_basket.delete()
            request.user.save()
            logger.debug("test message in making an order and clearing the basket")
            return HttpResponseRedirect(_('all_product'))
