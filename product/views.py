from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect, HttpResponse
from django.views.generic import ListView, DetailView , TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View, FormView
from django.core.paginator import Paginator
from .models import Product, ProductImages, Category, Memberships, UserMembership, Bidding
from django.db.models import Count
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import ProductForm, ImageForm, MembershipForm, UserMembershipForm, BiddingForm,AcceptBidForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from celery import shared_task
from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
from django.views.decorators.csrf import csrf_exempt
import json
# from django.contrib.gis.geoip2 import GeoIP2
# from django.views.generic import FormView
# from django.urls import reverse
# from paypal.standard.forms import PayPalPaymentsForm



# from .mixins import AictiveUserRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator




# Create your views here.d 
# @method_decorator(cache_page(10 * 2), name='dispatch')
class Productlist(ListView):
    model = Product 
    context_object_name = 'product_list'
    paginate_by = 1
    template_name ="Product/product_list.html"
   
    
    def get_context_data(self,  **kwargs):
        import datetime
        print(datetime.datetime.now())
        context = super(Productlist, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('q')
        productlist =Product.objects.filter(status='Active')
        if search_query:
            productlist = productlist.filter(Q(name__icontains = search_query))
        
        page = self.request.GET.get('page', 1)
        paginator = Paginator(productlist, self.paginate_by)
        try:
            productlist = paginator.page(page)
        except PageNotAnInteger:
            productlist = paginator.page(1)
        except EmptyPage:
            productlist = paginator.page(paginator.num_pages)

        # x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        # else:
        #     ip = self.request.META.get('REMOTE_ADDR')
        # g = GeoIP2()
        # country = g.country(ip)
        # city = g.city(ip)
        # device_type = ""
        # browser_type = ""
        # browser_version = ""
        # os_type = ""
        # os_version = ""
        # if self.request.user_agent.is_mobile:
        #     device_type = "Mobile"
        # if self.request.user_agent.is_tablet:
        #     device_type = "Tablet"
        # if self.request.user_agent.is_pc:
        #     device_type = "PC"
    
        # browser_type = self.request.user_agent.browser.family
        # browser_version = self.request.user_agent.browser.version_string
        # os_type = self.request.user_agent.os.family
        # os_version = self.request.user_agent.os.version_string



        context.update({
            'category_list': Category.objects.all(),
            'product_list':productlist,
        #     'ip':ip,
        #      "device_type": device_type,
        # "browser_type": browser_type,
        # "browser_version": browser_version,
        # "os_type":os_type,
        # "os_version":os_version,
        # 'country':country,
        # 'city':city
        })
        return context
   

class CategoryProduct(ListView):
    model = Product
    paginate_by = 1
    template_name ="Product/product_list.html"
    # category_list: Category.objects.all()
    
    def get_queryset(self):
        # product_list = Product.objects.all()
        category_slug = self.kwargs.get('category_slug')
        # category_obj = Category.objects.get(Category,slug=category_slug)
        category_obj = get_object_or_404(Category, slug=category_slug)
        product_list = Product.objects.filter(category=category_obj)
        return product_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['title'] = f'{category_slug} Products'
        context.update({
            'category_list': Category.objects.all()
            
        })
        return context


class Productdetail(DetailView):
    model = Product , ProductImages
    # slug_field = 'product_slug'
    template_name ="Product/product_detail.html"
    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs.get("product_slug"))
    

@login_required
def postadd(request):
    post_count = Product.objects.filter(owner=request.user.id).count()
    usermembership = UserMembership.objects.get(user=request.user)
    status_count = Product.objects.filter(status='Active').count()
    my_kwargs = dict(
    request='request',
    
)
    
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES,request=request)
        # if usermembership.membership.name == 'Free' and post_count==1:
        #     messages.error(request, 'Your plan doesnot support')
        #     return render(request, 'Product/addproduct.html', {'form':form})
        if status_count ==1:
            messages.error(request, 'Your plan doesnot support')
            # return render(request, 'Product/addproduct.html', {'form':form})
        
        if form.is_valid():
            product =form.save(commit=False) 
            product.owner = request.user
            product.images = request.FILES.getlist('images')[0]
            product.save()
            productimages = request.FILES.getlist('images')[1:]
            for image in productimages:
                
                photo = ProductImages(product=product, image=image)
                photo.save()
            messages.success(request,
                             "Posted!")
            messages.success(request, 'Your product has been added!')
            return redirect('/products')
        else: # form not valid so display message and retain the data entered
            form = ProductForm(request.POST,request=request)
            messages.success(request, 'Error in creating your product, the form is not valid!')
            return render(request, 'Product/addproduct.html', {'form':form})
    else: #the form has no data
        form = ProductForm(request=request) #produce a blank form
        
        return render(request, 'Product/addproduct.html', {'form':form,'post_count':post_count,'usermembership':usermembership, 'status_count':status_count})


# @login_required
class MyAds(LoginRequiredMixin,ListView):
    model = Product 
    context_object_name = 'product_list'
    paginate_by = 1
    template_name = "Product/myads_list.html"
    
    def get_queryset(self):
        # username = self.kwargs.get('username')
        # user_obj = get_object_or_404(User, username=username)
        product_list = Product.objects.filter(owner=self.request.user.id)
        post_count = Product.objects.filter(owner=self.request.user.id).count()
        return product_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['title'] = f'{username} Products'
        context['post_count']= Product.objects.filter(owner=self.request.user.id).count()
        return context


class UpdateProduct(UpdateView):
    model = Product
    slug_field = 'slug'
    form_class = ProductForm
    template_name = 'Product/update_ad.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request}) 
        return kwargs

    def get_success_url(self):
        return redirect('products:myads')

    def form_valid(self, form):
        productform = form.save(commit=False)
        productform.owner = self.request.user
        
        if self.request.FILES:
            productform.images = self.request.FILES.getlist('images')[0]
            productimages = self.request.FILES.getlist('images')[1:]
            productimages = self.request.FILES.getlist('images')[1:]
            for image in productimages:
                
                photo = ProductImages(product=productform, image=image)
                photo.save()
            
        self.object = productform
        self.object.save() 
        return redirect('products:myads')
          


class DeleteAdd(LoginRequiredMixin, DeleteView):

    model = Product
    def get_success_url(self):
        return redirect('products:myads')
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product_obj = get_object_or_404(Product, id=product_id)

        product_obj.delete()
        messages.success(request, f'{product_obj.id} Deleted Successfully Succesfully')
        return redirect('products:myads')


class MembershipView(ListView):
    model = Memberships
    template_name = 'Product/membership.html'
    

    def get_user_membership(self):
        
        user_membership_qs = UserMembership.objects.filter(user=self.request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None

    def get_context_data(self, *args, **kwargs):
        subcript = Memberships.objects.all()
        context = super().get_context_data(**kwargs)
        
        current_membership = self.get_user_membership()
        
        context['subcript'] = subcript
        context['curreproduct/<slug:slug>nt_membership'] = current_membership
        context['form'] = UserMembershipForm()
        
        member = UserMembership.objects.filter(user=self.request.user)
        context['usermembership']= member[0] if member else None

        return context
        
    def post(self, request):
        form = MembershipForm()
        form = UserMembershipForm()

class ChangeMembership(DetailView):
    model = Memberships
    template_name = 'Product/changemembership.html'
    def get_object(self, queryset=None):
        
        current = Memberships.objects.get(slug=self.kwargs.get("membership_slug"))
        
        user = UserMembership.objects.filter(user=self.request.user)
        if user:

            user = UserMembership.objects.get(user=self.request.user)
            user.membership = current
            user.save()
        else:
            user = UserMembership.objects.create(user=self.request.user,membership=current)
        return redirect('products:memberships')
    def get_context_data(self, *args, **kwargs):
       
        context = super().get_context_data(**kwargs)
        context['currentplan'] = current = Memberships.objects.get(slug=self.kwargs.get("membership_slug"))
        return context
        

def bidding(request,slug):
    
    
    if request.method=='POST':
        form = BiddingForm(request.POST, )
        if form.is_valid():
            bidding =form.save(commit=False) 
            bidding.user = request.user
           
            bidding.bid_product= Product.objects.get(slug=slug)
            bidding.save()
          
            return redirect('/products')
        else: # form not valid so display message and retain the data entered
            form = BiddingForm(request.POST)
            return render(request, 'Product/bidding.html',{'form':form})
    form = BiddingForm() #produce a blank form
    return render(request, 'Product/bidding.html', {'form':form})


class MyBidList(ListView):
    model = Bidding, Product
    context_object_name = 'mybidding_list'
    template_name = "Product/mybid_list.html"
    def get_queryset(self):
        mybidding_list = Bidding.objects.all()
        bid_product= Product.objects.get(slug=self.kwargs.get("slug"))
        return mybidding_list   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bid_product= Product.objects.get(slug=self.kwargs.get("slug"))
        context['mybidding_list']= Bidding.objects.filter(bid_product=bid_product)
        
        return context


class BidStatusUpdate(DetailView):
    model = Bidding, Product
    context_object_name = 'AcceptedBid'
    template_name = "Product/acceptedbid.html"
    

    def get_object(self, queryset=None):
        bidv= Bidding.objects.get(id=self.kwargs.get('id'))
        bidv.bid_status= self.kwargs.get('status')
       
        bidv.save()
        if bidv.bid_status == 'Accept':
            bid_s = Bidding.objects.filter(bid_product=bidv.bid_product, bid_status="Pending").update(bid_status="Reject")
        
            bidv.bid_product.status ='Complete'
            bidv.bid_product.save()
        
        

       
        return bidv
   





class MyAllBids(ListView):
    model = Bidding, Product
    context_object_name = 'myallbid_list'
    template_name = "Product/myallbid_list.html"


    def get_queryset(self):
        myallbid_list = Bidding.objects.all()
        # bid_product= Product.objects.get(slug=self.kwargs.get("slug"))
        return myallbid_list 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # bid_product= Product.objects.get(slug=self.kwargs.get("slug"))
        context['myallbid_list']= Bidding.objects.filter(user=self.request.user)
        
        return context

 




class GenerateRandomUserView(FormView):
    template_name = 'Product/randomusers.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('products:users_list')
    
    




class UsersListView(ListView):
    template_name = 'Product/user_list.html'
    model = User


#payment options






@csrf_exempt
def paypal_webhook(request):
   
    payload = request.body.decode('utf-8')
    event = None

    try:
        event = json.loads(payload)  
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    # except stripe.error.SignatureVerificationError as e:
    #     # Invalid signature
    #     return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    print(event['event_type'])
    if event['event_type'] == 'CHECKOUT.ORDER.APPROVED':
        # import pdb; pdb.set_trace()
        # print(event)
        # metadata = event['resource']['purchase_units'][0]
        # transaction = Transaction.objects.get(id=metadata['custom_id'])

        # if not UserSubscription.objects.filter(transaction=transaction).exists():
        #     user_subs = UserSubscription()
        #     user_subs.transaction = transaction
        #     user_subs.user = transaction.user
        #     user_subs.subscription_package = transaction.subscription_package
        #     user_subs.payment_status = 'paid'
        #     user_subs.active = True
        #     user_subs.start_date = datetime.now()
        #     user_subs.end_date = datetime.now() + timedelta(days=transaction.subscription_package.sub_period.days)
        #     user_subs.save()

        #     transaction.payment_status = 'paid'        
        #     transaction.save()
        
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)




  
def setcookie(request):  
    response = HttpResponse("Cookie Set")  
    response.set_cookie('Resel', 'resel.com')  
    return response  
def getcookie(request):  
    Resel  = request.COOKIES['Resel']  
    return HttpResponse("Resel cookies @: "+  Resel);  





def create_session(request):
    request.session['name'] = 'username'
    request.session['password'] = 'password123'
    return HttpResponse("<h1>dataflair<br> the session is set</h1>")
def access_session(request):
    response = "<h1>Welcome to Sessions of dataflair</h1><br>"
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))
        return HttpResponse(response)
    else:
        return redirect('create/')