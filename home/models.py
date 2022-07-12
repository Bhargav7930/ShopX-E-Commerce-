from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=12)
    auth_token = models.CharField(max_length=1200,default=0)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile',default=True)
    

    def __str__(self):
        return self.full_name

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name =models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')
    price = models.CharField(max_length=200)
    detail = models.TextField()
    slug = models.SlugField(unique=True,max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    def save(self,*args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args,**kwargs)

class Cart(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price =models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.username + " " +str(self.total_price)

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " "+ self.product.product_name

# @receiver(pre_save,sender=CartItem)
# def correct_price(self,**kwargs):
#     cart_items = kwargs['instance']
#     price_of_product = Product.objects.get(id=cart_items.product.id)
#     cart_items.price = cart_items.quantity * price_of_product.price
#     total_price = price_of_product.price * cart_items.quantity
#     cart = Cart.objects.get(user=cart_items.user,ordered=False).first()
#     cart.total_price = total_price
#     cart.save()

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200)
    payment_signature = models.CharField(max_length=200)

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    cart_item =models.ForeignKey(CartItem, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " "+ self.order.order_id

class Shipping_Address(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,default=0)
    email = models.EmailField(max_length=255,default=True)
    full_name = models.CharField(max_length=255,default=None)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name