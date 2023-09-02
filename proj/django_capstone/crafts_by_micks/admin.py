from django.contrib import admin
from .models import Product, Label, Category, Review, Product_Sizes, Option

# Register your models here.
admin.site.register(Product)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Product_Sizes)
admin.site.register(Option)

