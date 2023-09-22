from django.contrib import admin
from .models import Product, Product_Images, Label, Category, Review, Product_Sizes, Option, Order_Item, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Product_Images)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Product_Sizes)
admin.site.register(Option)
admin.site.register(Order_Item)
admin.site.register(Order)

