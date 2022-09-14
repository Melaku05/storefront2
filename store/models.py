from itertools import permutations
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from django.conf import settings


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
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
   
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
   
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    class Meta:
        '''
        Ordering by last_name and first_name
        '''
        ordering = ['user__first_name', 'user__last_name']


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

    class Meta:
        permissions = [
            ('cancel_order', 'can cancel order')
        ]
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
    id = models.UUIDField(primary_key=True, default=uuid4) #It is a passing reference, not just a calling function.
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    '''
    CartItem is a many-to-many relationship between Cart and Product.
    '''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

