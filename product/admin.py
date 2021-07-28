from django.contrib import admin
from .models import Product, Category, Brand, ProductImages, Memberships, UserMembership, Bidding

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImages)

admin.site.register(Memberships)
admin.site.register(UserMembership)
admin.site.register(Bidding)

