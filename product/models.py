from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django. utils import timezone
from django .utils.text import slugify
from django.urls import reverse
from django.db.models import signals
from django.dispatch import dispatcher
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    status_choices = (('Active', 'Active'),
        ('Pending', 'Pending'), 
       ('Complete', 'Complete'),
        )
    status = models.CharField(max_length = 100, choices = status_choices, default="Pending")
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)
    class Meta:
        ordering = ['id']

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

#membership or subscription choice
MEMBERSHIP_CHOICES = (('Premium', 'pre'),('Free', 'free'))
#class for membership with slug where slug is used to define type of membership
# class Membership(models.Model):
#     slug = models.SlugField(null=True, blank=True)
#     membership_type = models.CharField(
#     choices=MEMBERSHIP_CHOICES, default='Free',
#     max_length=30
#       )
#     price = models.DecimalField(max_digits=15,decimal_places=2,default=0)
#     def __str__(self):
#        return self.membership_type

#class for usermembership where membership is foregin key to Membership Class and user is User in django.contrib.auth
class UserMembership(models.Model):
    user = models.OneToOneField(User,related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey('Memberships', related_name='user_membership', on_delete=models.CASCADE, null=True)
    def __str__(self):
       return self.membership.name + " " + self.user.username



class Memberships(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    def __str__(self):
       return self.name


class Bidding(models.Model):
    user = models.ForeignKey(User, related_name='bid_owner', on_delete=models.CASCADE)
    bidding_amount = models.DecimalField(max_digits=15,decimal_places=2)
    bid_product = models.ForeignKey(Product,related_name="bid_product",on_delete=models.CASCADE )
    status_choices = (('Accept', 'Accept'),('Reject', 'Reject'),('Pending', 'Pending'),)
    bid_status = models.CharField(max_length = 100, choices = status_choices, default="Pending")
    
    def __str__(self):
       return self.bid_product.name
    #    return str(self.bid_product.Product.name)




@receiver(post_save, sender=User)
def Usermembershipsignal(sender, instance, created,**kwargs):



    if created:
    
        # user = User.objects.get(username=instance.username)
        membership = Memberships.objects.get(slug='free')
        usermembership = UserMembership.objects.create(user=instance,membership=membership)

            
    