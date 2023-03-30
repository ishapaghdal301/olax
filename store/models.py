from django.db import models
import datetime
  
  
class Category(models.Model):
    name = models.CharField(max_length=50)
  
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    def get_category_id(id):
        return Category.objects.filter(id=id)
  
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    pass1 = models.CharField(max_length=100)
    pass2 = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=True)
    gender = models.CharField(max_length=10,null=True)
    nationality = models.CharField(max_length=20,null=True)
    upload = models.ImageField(upload_to ='prof_image',default='mob1.png',null = True)
    address = models.CharField(max_length=100,null=True)
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def get_customer_by_username(username):
        try:
            return Customer.objects.get(username=username)
        except:
            return False

    @staticmethod
    def get_customer_by_id(id):
        try:
            return Customer.objects.get(id = id)
        except:
            return False
  
    def isExists(self):
        if Customer.objects.filter(username=self.username):
            return True
  
        return False
    
    def __str__(self):
        return self.username
    
class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='products' ,default='mob1.png', null = True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,default=1)
    
    def register(self):
        self.save()

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)
    
    @staticmethod
    def get_product_by_id(id):
        return Products.objects.get(id = id)
        
    @staticmethod
    def get_products_by_customer(ids):
        return Products.objects.filter(customer=ids)
  
    @staticmethod
    def get_all_products():
        return Products.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()
        
class Order(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')