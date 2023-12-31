"""Models for Django App 'crafts_by_micks' for Product, Order and associated Attributes Creation

Classes:
--------
:class: `Label`
:class: `Category`
:class: `Product`
:class: `Product_Images`
:class: `Option`
:class: `Product_Sizes`
:class: `Review`
:class: `Order`
:class: `Order_Item`
"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Label(models.Model):
    """Class modeling a Product Label ('new', 'discount', etc).
        Many-To-One relationship with class `Product`.

    Attributes:
    -----------
    title: str (CharField)
        title (name) of label
    discount_percentage: int (IntegerField)
        percentage of discount to be applied to a product (applied to all sizes)
    creation_date: DateField()
        Date of Product Creation
    removal_days: int (IntegerField)
        optional number of days after which label must be removed from a product
    custom_colour: str (Charfield)
        user chosen colour (default light blue) for label background

    Methods:
    --------
    :meth:`__str__(self)`
        :return: `Label` title
        :rtype: str
    """
    title = models.CharField(max_length=20, unique=True)
    discount_percentage = models.IntegerField(null=True)
    creation_date = models.DateField()
    removal_days = models.IntegerField(null=True)
    # default colour set to 'light blue'
    custom_colour = models.CharField(max_length=10, null = True, default="#89CFF0")

    def __str__(self):
        """Return title of Label.
            :return: `Label` title
            :rtype: str
        """
        return self.title


class Category(models.Model):
    """Class modeling a Product Category.
        'create_product.html' set to maintain One-To-One Relationship.

    Attributes:
    -----------
    title: str (CharField)
        title (name) of Category

    Methods:
    --------
    :meth:`__str__(self)`
        :return: `Category` title
        :rtype: str
    """
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Return Title of Category.
        
            :return: `Category` title
            :rtype: str
        """
        return self.title


class Product(models.Model):
    """Class modeling a Product.
        Size Variations handled within Product and should not form part of name.

    Attributes:
    -----------
    title - str (CharField)
        title (name) of Product
    description: str (TextField):
        A description of the current Product
    review_vaue: int (IntegerField)
        review rating of product - default value set to 0. Functionality allowing
        admin (not superuser) to modify review in any way has not been added.
    product_image: models.ImageField
        main image for product
    labels: Label
        Associated Label objects for Product
    category: Category
        Associated Category for Product

    Methods:
    --------
    :meth:`__str__(self)`
        :return: `Product` title
        :rtype: str
    """
    title = models.TextField(unique = True)
    description = models.TextField()
    review_value = models.FloatField(default = 0.0)
    product_image = models.ImageField(upload_to= 'products_images/', default=None)
    labels = models.ManyToManyField(Label)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        """Return Title of Product.
            :return: `Product` title
            :rtype: str
        """
        return self.title


class Product_Images(models.Model):
    """Class to hold instances containing images assigned to a Product.
        Set to delete the image upon deletion of the product

    Attributes:
    -----------
    product: Product 
        Associated Product Object
    image: ImageField
        admin user desired product image (formats currently set to .gif, .png and .jpg
        in html form to create_product)

    Methods:
    --------
    :meth:`__str__(self)`
        :return: Image Primary Key and Assigned `Product` Title
        :rtype: int
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'products_images/', default=None)

    def __str__(self):
        """
        :return: Image Primary Key and Assigned `Product` Title
        :rtype: int
        """
        return str(f"id: {self.id}, product: {self.product.title}")

class Option(models.Model):
    """Class modeling Options for a Product.
        Any design variation or detailed product execution such as a
        style change, scented, material variation, etc.
        Cascading Deletion with associated Product.

    Attributes:
    -----------
    product: Product
        Associated Product Object
    title: str (CharField)
        Name of Product
    description: str (Charfield)
        A short description giving detail of the Option

    Methods:
    --------
    :meth:`__str__(self)`
        :return: Associated `Product` id and `Option` title
        :rtype: str
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        """
        :return: Associated `Product` id and `Option` title
        :rtype: str
        """
        return f"Product: {self.product.id}, {self.title}"


class Product_Sizes(models.Model):
    """Class modeling Size_Options for a Product with corresponding price.
        No size option taken as 'none'.
        Cascading Deletion from associated Product.

    Attributes:
    -----------
    product: Product
        Associated Product Object
    size_options: tuple
        contains tuples for each product size
    size: str (Charfield)
        selected size for Product
    price: float
        price for Product according to size

    Methods:
    --------
    :meth:`__str__(self)`
        :return: `Product` id, size and price
        :rtype: str
    """
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    size_options = (
        ('n', 'none'),
        ("xs", "extra-small"),
        ("sm", "small"),
        ("m", "medium"),
        ("lg", "large"),
        ("xl-large", "extra-large"),
        ("xxl", "XXL")
    )

    size = models.CharField(max_length=15, choices=size_options)
    price = models.FloatField(default=0.0)

    def __str__(self):
        """
        :return: `Product` id, size and price
        :rtype: str
        """
        return f"Product: {self.product.id}, {self.size}, {self.price}"


class Review(models.Model):
    """Class modeling a Review for a Product.

    Attributes:
    -----------
    product: Product
        Associated Product Object
    author: str (Charfield)
        name of person writing review
    description: str (TextField)
        review content
    rating: int (IntegerField)
        review rating

    Methods:
    --------
    :meth:`__str__(self)`
        :return: author and review id
        :rtype: str
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.TextField(max_length=200)
    description = models.TextField(null=True)
    rating = models.IntegerField()

    def __str__(self):
        """
        :return: author and review id
        :rtype: str
        """
        return f"{self.author}, Review No: {self.id}"

class Order(models.Model):
    """Class Modelling a Single Order for a customer.

    Attributes:
    -----------
    customer: Django User
        Authenticated and Logged-In Customer placing order
    submitted_date: DateTimeField
        date for order submission to be processed
    payment_received_date: DateTimeField
        date payment was received for order
    delivered_date: DateTimeField
        date order was delivered to customer
    total_value: FloatField
        tracked total value for order
    status: CharField (str)
        description of order status from not yet completed by
        customer to completed and delivered

    Method:
    -------
    :meth:`__str__(self)`
        :return: `Order` id, customer name and `Order` status
        :rtype: str
    """
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    submitted_date = models.DateField(null=True, blank=True)
    payment_received_date = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    total_value = models.FloatField(default=0)

    status_options = (
        ('ns','not_submitted'),
        ('r', 'receieved'),
        ('p', 'paid'),
        ('c', 'completed')
    )

    status = models.CharField(max_length=20, choices=status_options)

    def __str__(self):
        """
        :return: `Order` id, customer name and `Order` status
        :rtype: str
        """
        return str(f'Order: {self.id}, Customer: {self.customer.first_name}, status: {self.status}')


class Order_Item(models.Model):
    """Class modeling an Item to be added to an Order.

    Attributes:
    -----------
    order: Order
        assigned order for this product Item
    product_id: IntegerField
        unique id of product being added to an order
    product_title: TextField (str)
        title of product being added to an order
    quantity: IntegerField
        quantity of a product being ordered
    chosen_size: TextField
        description of the size being chosen
    price: FloatField
        price of product matching a chosen size
    options: TextField (str)
        description of specified options for a product

    Methods:
    --------
    :meth:`__str__(self)`
        :return: `Product` title
        :rtype: str
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default=None)
    product_id = models.IntegerField()
    product_title = models.TextField(max_length = 200)
    quantity = models.IntegerField()
    chosen_size = models.TextField()
    price = models.FloatField(max_length=30)
    options = models.TextField(default=None)

    def __str__(self):
        """
        :return: `Product` title
        :rtype: str
        """
        return f"Order for Product: {self.product_title}"
