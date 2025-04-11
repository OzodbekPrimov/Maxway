from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *

admin.site.register(Category)
# admin.site.register(Order)
# admin.site.register(OrderProduct)
# admin.site.register(Customer)
# admin.site.register(Product)

@admin.register(OrderProduct)
class OrderProductAdmin(ModelAdmin):
    list_display = ('product__title', 'count', 'price',  'order__id')
    list_filter = ('count', )
    ordering = ('created_at', )



@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'customer__first_name', 'payment_type', 'status', 'address', 'created_at')
    list_filter = ('payment_type', 'status', 'created_at')
    ordering = ("created_at",)



@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('id', 'title', 'price', 'category__title', 'image')
    search_fields = ('title', 'description')
    list_filter = ('category', )
    ordering = ('id',)


@admin.register(Customer)
class CustomUserAdmin(ModelAdmin):
    list_filter = ('first_name', 'phone_number')
    ordering = ('created_at',)