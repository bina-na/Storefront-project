from django.db import models
# Create your models here.
class promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    feature_product = models.ForeignKey('product' , on_delete=models.SET_NULL , null =True, related_name='+')


class product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)
    last_update = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(Collection , on_delete= models.PROTECT )
    promotion = models.ManyToManyField(promotion)   

class customer(models.Model):
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
    birth_day = models.DateField(null=True)
    membership = models.CharField(max_length=1 ,choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    class Meta:
        indexes = [
            models.Index(fields =['last_name', 'first_name'])
        ]

class order(models.Model):
    PAYMENT_STATUS_PENDING = 'P' 
    PAYMENT_STATUS_COMPELET = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING , 'Pending'),
        (PAYMENT_STATUS_COMPELET, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default= PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(customer , on_delete= models.PROTECT ) 

class OrderItem(models.Model):
    order = models.ForeignKey(order , on_delete=models.PROTECT)
    product = models.ForeignKey(product , on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places= 2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(product , on_delete= models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(customer , on_delete=models.CASCADE, primary_key= True)

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    