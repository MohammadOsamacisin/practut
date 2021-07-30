from django.urls import path
from . import views
from .views import Productlist , Productdetail,MyAds, paypal_webhook



app_name = 'product'
urlpatterns = [
    # path('',views.productlist, name="productlist"),
    path('',views.Productlist.as_view(), name= 'productlist'),
    path('category/<slug:category_slug>/',views.CategoryProduct.as_view(), name= 'product_list_category'),
    #  path('<slug:product_slug>',views.productdetail,name= "product_detail"),
    path('detail/<slug:product_slug>/',views.Productdetail.as_view(),name= "product_detail"),
    path('post-ad/', views.postadd, name='post_ad'),
    # path('post-ad/', views.PostAd.as_view(), name='post_ad'),
    path('myads/',views.MyAds.as_view(),name ="myads"),
    path('delete-ad/<int:id>', views.DeleteAdd.as_view(), name='delete_ad'),
    path('update/product/<slug:slug>/',views.UpdateProduct.as_view(), name="update_product"),
    path('memberships/', views.MembershipView.as_view(), name='memberships'),
    path('changemembership/<slug:membership_slug>/',views.ChangeMembership.as_view(),name= "changemembership"),
    path('bidding/<slug:slug>', views.bidding, name='bidding'),
    path('mybids/<slug:slug>',views.MyBidList.as_view(),name ="mybids"),
    # path('bidacceptor/',views.BidAcceptor.as_view(),name ="bidacceptor"),
    path('bidstatusupdate/<int:id>/<str:status>',views.BidStatusUpdate.as_view(),name ="bidstatusupdate"),
    # path('bidrejector/<int:id>',views.BidRejector.as_view(),name ="bidrejector"),
    path('myallbids/',views.MyAllBids.as_view(),name ="myallbids"),
    path('generate/', views.GenerateRandomUserView.as_view(), name= 'generate'),
    path('userlist/',views.UsersListView.as_view(),name= 'users_list'),
    path('webhooks/', views.paypal_webhook, name= 'successwebhook'),
    path('setcookies/', views.setcookie, name= 'setcookies'),
    path('getcookies/', views.getcookie, name = 'getcookie'),
    path('create/', views.create_session, name= 'createsession'),
    path('access/', views.access_session, name= 'access_session'),



]
