from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Basket, PartBasket, UsersOrderHistory, PartUsersOrderHistory


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('first_name', 'last_name', 'balance_user', 'total_expenses', 'status')
    list_editable = ('balance_user', 'total_expenses')
    fieldsets = (
        ('These fields can be edited', {
            'fields': ('first_name', 'last_name', 'balance_user', 'total_expenses', 'user_basket', 'user_order_history')
        }),
        ('These fields cannot be edited', {
            'fields': ('status',)
        }),
    )


class BasketAdmin(admin.ModelAdmin):
    model = Basket
    list_display = ('pk',)
    list_display_links = ('pk',)


class PartBasketAdmin(admin.ModelAdmin):
    model = PartBasket
    list_display = ('pk', 'product', 'quantity_product')
    list_display_links = ('pk', 'product', 'quantity_product')


class UsersOrderHistoryAdmin(admin.ModelAdmin):
    model = UsersOrderHistory
    list_display = ('pk',)
    list_display_links = ('pk',)


class PartUsersOrderHistoryAdmin(admin.ModelAdmin):
    model = PartUsersOrderHistory
    list_display = ('pk', 'product', 'quantity_product')
    list_display_links = ('pk', 'product', 'quantity_product')


admin.site.register(PartUsersOrderHistory, PartUsersOrderHistoryAdmin)
admin.site.register(UsersOrderHistory, UsersOrderHistoryAdmin)
admin.site.register(PartBasket, PartBasketAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
