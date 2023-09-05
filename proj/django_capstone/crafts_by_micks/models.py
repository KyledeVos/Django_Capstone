from django.db import models

# Create your models here.

class Label(models.Model):
    title = models.CharField(max_length=20)
    discount_percentage = models.IntegerField(null=True)
    creation_date = models.DateField()
    removal_days = models.IntegerField(null=True)
    custom_colour = models.CharField(max_length=10, null = True, default="#89CFF0") # default light blue

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.FloatField()

    quantity = models.IntegerField()
    review_value = 0.0
    # field for main image
    # field for other product images
    labels = models.ManyToManyField(Label)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Product: {self.product.id}, {self.title}"
    

class Product_Sizes(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    size_options = (
        ("xs", "extra-small"),
        ("sm", "small"),
        ("m", "medium"),
        ("lg", "large"),
        ("xl-large", "extra-large"),
        ("xxl", "XXL")
    )

    size = models.CharField(max_length=15, choices=size_options)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"Product: {self.product.id} {self.size}"



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.TextField(max_length=200)
    description = models.TextField(null=True)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.author}, Review No: {self.id}"
    
