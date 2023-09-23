"""Models for Django App 'crafts_by_micks' for Product, Order and associated Attributes Creation

Classes:
--------
Label
Category
Product
Product_Images
Option
ProductSizes
Review
Order
Order_Item
"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Label(models.Model):
    """Class modeling a Product Label ('new', 'discount', etc). Product to have Many-To-One
        Relationship allowing one Product to have many Labels.
    Child class of django models.Model.

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
    __str__(self): str
        return title of label
    """
    title = models.CharField(max_length=20, unique=True)
    discount_percentage = models.IntegerField(null=True)
    creation_date = models.DateField()
    removal_days = models.IntegerField(null=True)
    # default colour set to 'light blue'
    custom_colour = models.CharField(max_length=10, null = True, default="#89CFF0")

    def __str__(self):
        """Return title of Label"""
        return self.title


class Category(models.Model):
    """Class modeling a Product Category. Each Product should belong to one Category, however
        Many-To-One Relationship set instead for possible future changes. 'create_product.html'
        currently set to maintain One-To-One Relationship. Child class of django models.Model.

    Attributes:
    -----------
    title: str (CharField)
        title (name) of Category

    Methods:
    --------
    __str__(self): str
        return title of Category
    """
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        "Return Title of Category"
        return self.title


class Product(models.Model):
    """Class modeling a Product . Size Variations are handled within Product and should
        not form part of name. Child class of django models.Model.

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
    __str__(self): str
        return title of Product
    """
    title = models.CharField(max_length=200, unique = True)
    description = models.TextField()
    review_value = 0.0
    product_image = models.ImageField(upload_to= 'products_images/', default=None)
    labels = models.ManyToManyField(Label)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        """Return Title of Product"""
        return self.title


class Product_Images(models.Model):
    """Class to hold instances containing images assigned to a Product, set to delete the
    image upon deletion of the product

    Attributes:
    -----------
    product: Product 
        Associated Product Object
    image: ImageField
        admin user desired product image (formats currently set to .gif, .png and .jpg
        in html form to create_product)

    Methods:
    --------
    __str__(self): str
        return primary key of image and name of product assigned to
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'products_images/', default=None)

    def __str__(self):
        return str(f"id: {self.id}, product: {self.product.title}")

class Option(models.Model):
    """Class modeling Options for a Product.
        An Option is consider as any design variation or detailed product execution
        such as a style change, scented, material variatoion, etc. Cascading Deletion with
        associated Product.

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
    __str__(self): str
        return Associated product id and title of Option
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        """return Associated product id and title of Option"""
        return f"Product: {self.product.id}, {self.title}"
    

class Product_Sizes(models.Model):
    """Class modeling Size_Options for a Product with corresponding price.
        Products with no size option take size as 'none'. Cascading Deletion
        from associated Product.

    Attributes:
    -----------
    product: Product 
        Associated Product Object
    size_options: tupple
        contains tuples for each product size
    size: str (Charfield)
        selected size for Product
    price: float
        price for Product according to size

    Methods:
    --------
    __str__(self): str
        return Product id and size
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
    price = models.FloatField(default=0)

    def __str__(self):
        """return Product id and size"""
        return f"Product: {self.product.id} {self.size} {self.price}"


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
    __str__(self): str
        return author and id of review
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.TextField(max_length=200)
    description = models.TextField(null=True)
    rating = models.IntegerField()

    def __str__(self):
        """ return author and id of review"""
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
    def __str__(self):
        "Return Description of Order"
    """
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    submitted_date = models.DateTimeField(null=True, blank=True)
    payment_received_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    total_value = models.FloatField(default=0)

    status_options = (
        ('ns','not_submitted'),
        ('r', 'receieved'),
        ('p', 'paid'),
        ('c', 'completed')
    )

    status = models.CharField(max_length=20, choices=status_options)

    def __str__(self):
        "Return Description of Order"
        return str(f'Order: {self.id}, Customer: {self.customer.first_name}, status: {self.status}')


class Order_Item(models.Model):
    """Class modeling an Item to be added to an Order for a customer (user).

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
    __str__(self): str
        return author and id of review
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default=None)
    product_id = models.IntegerField()
    product_title = models.TextField(max_length = 200)
    quantity = models.IntegerField()
    chosen_size = models.TextField()
    price = models.FloatField(max_length=30)
    options = models.TextField(default=None)

    def __str__(self):
        """ return customer_name and product title selected"""
        return f"Order for Product: {self.product_title}"
    
