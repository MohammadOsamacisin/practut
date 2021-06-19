from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django. utils import timezone
from django .utils.text import slugify
# Create your models here.
class Product(models.Model):
    ConditionType=(
        ("New","New"),
        ("Used","Used")
    )
    # it will store product information
    name = models.CharField(max_length=100)
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=700)
    condition= models.CharField(max_length=200, choices=ConditionType)
    category= models.ForeignKey('Category',on_delete=models.SET_NULL, null=True)
    brand= models.ForeignKey('Brand',on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    images= models.ImageField(upload_to='main_product/', blank= True, null=True)
    created= models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)

    
    
    def __str__(self):
        return self.name
#class for product images
class ProductImages(models.Model):
    product=models.ForeignKey(Product,related_name="productimages",on_delete=models.CASCADE )
    image= models.ImageField(upload_to='products/',blank= True, null=True)
    class Meta:
        verbose_name='Product Image'
        verbose_name_plural='Product Images'
    
    

    def __str__(self):
        return self.product.name

class Category(models.Model):
    # category of item particular
    category_name = models.CharField(max_length=100)
    logo= models.ImageField(upload_to='category/', blank= True, null=True)
    slug = models.SlugField(blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)


    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    def __str__(self):
        return self.category_name


class Brand(models.Model):
    # subcategory of item particular
    brand_name = models.CharField(max_length=100)
   # image= models.ImageField(upload_to='products/', blank= True, null=True)


    class Meta:
        verbose_name='brand'
        verbose_name_plural='brands'
    def __str__(self):
        return self.brand_name

