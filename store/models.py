from itertools import product
from unicodedata import name
from django.core.validators import MinValueValidator
from django.db import models


class Promotion(models.Model):
    '''
    Promotion model
    '''
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    '''
    The title of the collection.
    '''
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def _str_(self) -> str:
        return self.title

    class Meta:
        '''
        Meta class for Collection model
        '''
        ordering = ['title']


class Product(models.Model):
    '''
    The title of the product.
    '''
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def _str_(self) -> str:
        '''
        Return the title of the product.
        '''
        return self.title

    class Meta:
        '''
        The ordering is based on the title field.
        '''
        ordering = ['title']


class Customer(models.Model):
    '''
    The Customer model has a one-to-many relationship with the Order model.
    '''
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        '''
        Ordering by last_name and first_name
        '''
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    '''
    Order model
    '''
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    '''
    OrderItem is a many-to-many relationship between Order and Product.
    '''
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    '''
    Address is a many-to-one relationship between Customer and Order.
    '''
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    '''
    Cart is a many-to-one relationship between Customer and Order.
    '''
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    '''
    CartItem is a many-to-many relationship between Cart and Product.
    '''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)