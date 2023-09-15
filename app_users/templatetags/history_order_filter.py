from django import template
from ..models import CustomUser

register = template.Library()


@register.simple_tag()
def history_order_filter():
    all_order = CustomUser.get_order_history()
    most_popular_product = dict()

    for qwe in all_order:
        if qwe.product not in most_popular_product:
            most_popular_product[qwe.product] = qwe.quantity_product
        else:
            most_popular_product[qwe.product] += qwe.quantity_product

    sorted_dict = dict(sorted(most_popular_product.items(), key=lambda x: -x[1]))
    return sorted_dict
