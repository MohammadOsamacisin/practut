from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect
from django.views.generic import ListView, DetailView , TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from .models import Product, ProductImages, Category
from django.db.models import Count
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import ProductForm, ImageForm
from django.contrib.auth.decorators import login_required
# from .forms import AdPostForm
# from accounts.mixins import AictiveUserRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class Productlist(ListView):
    model = Product 
    context_object_name = 'product_list'
    paginate_by = 1
    # productlist =Product.objects.all() 
    # search_query= ""
        # return super(Productlist,self).get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(Productlist, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('q')
        productlist =Product.objects.all()
        if search_query:
            productlist = productlist.filter(
                Q(name__icontains = search_query)
            )

        page = self.request.GET.get('page', 1)
        
        paginator = Paginator(productlist, self.paginate_by)
        try:
            productlist = paginator.page(page)
        except PageNotAnInteger:
            productlist = paginator.page(1)
        except EmptyPage:
            productlist = paginator.page(paginator.num_pages)
        context.update({
            'category_list': Category.objects.all(),
            'product_list':productlist
        })
        return context
    # def get(self, request, *args, **kwargs):
    #     search_query = request.GET.get('q')
    #     if search_query:
    #         print(search_query)
    #     # return render(request,'Product/product_list.html')
   
    
   

class CategoryProduct(ListView):
    model = Product
    paginate_by = 1
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
    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs.get("product_slug"))
    
# class SearchView(ListView):
#     model = Product
#     def get(self, request, *args, **kwargs):
#         search_query = request.GET.get('q')
#         if search_query:
        
            
#             print(search_query)
#         return None
# class SearchProduct(ListView):
#     def get(self, request, *args, **kwargs):
#         area = request.GET.get('area')
#         city = request.GET.get('city')
#         search = request.GET.get('search')
#         category_id = request.GET.get('category')
#         category_obj = get_object_or_404(Category, id=category_id)

#         category_products = category_obj.category_products.all()

#         search_products = category_products.filter(
#             Q(title__icontains=search) | Q(description__icontains=search), city=city, area=area)

#         context = {
#             'title': 'Search Result',
#             'search_products': search_products
#         }

#         return render(request, 'Product/product_list.html', context)
@login_required
def postadd(request):
    ImageFormSet = modelformset_factory(ProductImages,
                                        form=ImageForm, extra=3)
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=ProductImages.objects.none())
        if form.is_valid():
            product =form.save() 
            for form in formset.cleaned_data:
                image = form['image']
                import pdb;
                pdb.set_trace()
                photo = ProductImages(product=product, image=image)
                photo.save()
            messages.success(request,
                             "Posted!")
            messages.success(request, 'Your product has been added!')
            return redirect('/products')
        else: # form not valid so display message and retain the data entered
                form = ProductForm(request.POST)
                messages.success(request, 'Error in creating your product, the form is not valid!')
                return render(request, 'Product/addproduct.html', {'form':form})
    else: #the form has no data
        form = ProductForm() #produce a blank form
        formset = ImageFormSet(queryset=ProductImages.objects.none())
        return render(request, 'Product/addproduct.html', {'form':form,'formset':formset})
# class PostAd( View):
#     def get(self, request, *args, **kwargs):
#         ad_post_form = AdPostForm()
#         context = {
#             'title': 'Ad Post',
#             'ad_post_form': ad_post_form
#         }

#         return render(request, 'Product/post_ad.html', context)

#     def post(self, request, *args, **kwargs):
#         ad_post_form = AdPostForm(request.POST, request.FILES)

#         if ad_post_form.is_valid():
#             ad_post = ad_post_form.save()
#             ad_post.owner = request.user
#             ad_post.save()

#             for afile in request.FILES.getlist('images'):
#                 ad_post.product_images.create(image=afile)

#             messages.success(request, 'Ad Posted Succesfully')
#             return redirect('products:post_ad')
#         else:
#             context = {
#                 'title': 'Ad Post',
#                 'ad_post_form': ad_post_form
#             }

#             return render(request, 'Product/post_ad.html', context)

