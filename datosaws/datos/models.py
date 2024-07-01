from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import User

# from multiselectfield import MultiSelectField


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address_id = models.AutoField(primary_key=True)
    address_area = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    province = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
            verbose_name_plural = 'Address Book'

    def __str__(self):
        return self.address_area

class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    supplier_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    email = models.EmailField(null=True,blank=True)
    address_area = models.ForeignKey(Address, on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return self.company_name

CATEGORY_TYPE = [
('Bank', 'Bank'),
('Accounts Recievable', 'Accounts Recievable'),
('Other Current Assets', 'Other Current Assets'),
('Fixed Asset', 'Fixed Asset'),
('Other Asset', 'Other Asset'),
('Other Current Liability', 'Other Current Liability'),
('Long Term Liability', 'Long Term Liability'),
('Equity', 'Equity'),
('Income', 'Income'),
('Cost of Goods Sold', 'Cost of Goods Sold'),
('Expenses', 'Expenses'),
('Other Income', 'Other Income'),
]    
class Category(models.Model):
  category_type = models.CharField(max_length=100,blank=True,null=True, choices=CATEGORY_TYPE)
  category_name = models.CharField(max_length=100,blank=True,null=True)
  description = models.TextField(blank=True,null=True)

  class Meta:
            verbose_name_plural = 'Categories'

  @property
  def short_description(self):
         return truncatechars(self.description,70)

  def __str__(self):
        return self.category_name

PRODUCT_TYPE = [
('Equipment', 'Equipment'),
('Agriculture', 'Agriculture'),
('Cosmetics/Beauty', 'Cosmetics/Beauty'),
('Health', 'Health'),
('Materials', 'Materials'),
('Electronic', 'Electronic'),
('Clothing', 'Clothing'),
('Software', 'Software'),
('Service', 'Service'),
]

CURRENCY = [
('USD', 'USD'),
('ZMW', 'ZMW'),
('ZAR', 'ZAR'),
('GBP', 'GBP'),
]
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    currency = models.CharField(max_length=3,blank=True,null=True, choices=CURRENCY)
    quantity = models.IntegerField()
    product_type = models.CharField(max_length=100,blank=True,null=True, choices=PRODUCT_TYPE)
    company_name = models.ForeignKey(Supplier, on_delete=models.CASCADE,blank=True,null=True)
    photo = models.ImageField(null=True,blank=True, upload_to="images/")

    class Meta:
            verbose_name_plural = 'Products'
    @property
    def short_description(self):
         return truncatechars(self.description,50)

    @property
    def total_value(self):
         total_value = self.price*self.quantity
         return '{:,.2f}'.format(total_value)
    
    def item_photo(self):
         return mark_safe(f'<img scr="{self.photo.url}" width="100" height="100" />')

    item_photo.short_description = 'Image'

    def __str__(self):
        return self.name

PAYMENT_METHOD = [
('Cash', 'Cash'),
('Card', 'Card'),
('Credit', 'Credit'),
('Airtel Money', 'Airtel Money'),
('MTN Money', 'MTN Money'),
('Other', 'Other')
]


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    receipt_photo = models.ImageField(null=True,blank=True, upload_to="images/")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    company_name = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,blank=True)
    category_name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD,null=True,blank=True)
    

    class Meta:
        verbose_name_plural = 'Expenses'
    @property
    def short_description(self):
         return truncatechars(self.description,50)
    def __str__(self):
        return self.name
    

PAYMENT_METHOD = [
('Cash', 'Cash'),
('Card', 'Card'),
('Credit', 'Credit'),
('Airtel Money', 'Airtel Money'),
('MTN Money', 'MTN Money'),
('Other', 'Other')
]


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    company_name = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,blank=True)
    category_name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD,null=True,blank=True)
    

    class Meta:
        verbose_name_plural = 'Income'
    @property
    def short_description(self):
         return truncatechars(self.description,50)
    def __str__(self):
        return self.name

