from django.contrib import admin
from .models import ProductModel, ShopForProduct
from django.utils.translation import gettext_lazy as _


class ProductModelAdmin(admin.ModelAdmin):
    class PriceFilter10k(admin.SimpleListFilter):
        title = _('price filter')
        parameter_name = 'price_filter'

        def lookups(self, request, model_admin):
            return (
                ('<=10k', _('less 10000')),
                ('>10k', _('more 10000')),
            )

        def queryset(self, request, queryset):
            if self.value() == '<=10k':
                return queryset.filter(price__gte=0,
                                       price__lte=10_000)
            if self.value() == '>10k':
                return queryset.filter(price__gte=10_001,
                                       price__lte=999_999_999)

    @admin.action(description='Update product price __test__')
    def update_product_price_test(self, request, queryset):
        queryset.update(price=-1)

    model = ProductModel
    list_display = ('pk', 'title', 'description', 'price', 'specifications', 'quantity_product_in_shop')
    list_display_links = ('pk', 'title')
    search_fields = ('title', 'description')
    list_editable = ('price', 'quantity_product_in_shop')
    list_filter = (PriceFilter10k, 'created_at', 'price', 'quantity_product_in_shop')
    save_on_top = True
    readonly_fields = ('pk', 'created_at', 'updated_at',)
    actions = ('update_product_price_test',)
    empty_value_display = '-empty-'
    exclude = ('updated_at',)
    fieldsets = (
        ('These fields can be edited', {
            'fields': ('title', 'description', 'price', 'specifications', 'shop', 'quantity_product_in_shop')
        }),
        ('These fields cannot be edited', {
            'fields': ('pk',
                       ('created_at', 'updated_at'))
        }),
    )
    list_max_show_all = 20
    list_per_page = 20


class ShopForProductAdmin(admin.ModelAdmin):
    model = ShopForProduct
    list_display = ('title', 'description')
    list_display_links = ('title', 'description')
    search_fields = ('title',)


admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(ShopForProduct, ShopForProductAdmin)
