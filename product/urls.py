from django.urls import path
from . import views
from .views import Productlist , Productdetail
app_name = 'product'
urlpatterns = [
    # path('',views.productlist, name="productlist"),
    path('',views.Productlist.as_view(), name= 'productlist'),
    path('category/<slug:category_slug>/',views.CategoryProduct.as_view(), name= 'product_list_category'),
    #  path('<slug:product_slug>',views.productdetail,name= "product_detail"),
    path('detail/<slug:product_slug>/',views.Productdetail.as_view(),name= "product_detail"),
    path('post-ad/', views.postadd, name='post_ad'),
    # path('post-ad/', views.PostAd.as_view(), name='post_ad'),

]
