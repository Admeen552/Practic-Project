from django.contrib import admin
from .models import Category, Manufacturer, Product, WarehouseStock, Promocode, OrderStatus, Order, OrderItem, CartItem, Review

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(WarehouseStock)
admin.site.register(Promocode)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Review)