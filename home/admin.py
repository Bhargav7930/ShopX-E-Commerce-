from django.contrib import admin
from .models import Product,Category,Customer,CartItem,Contact,Cart,Order,OrderItem,Shipping_Address

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Shipping_Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact)