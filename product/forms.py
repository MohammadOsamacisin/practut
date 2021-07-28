from django import forms
from django.forms import ModelForm
from .models import Category, Product, ProductImages, Memberships, UserMembership, Bidding
from django.contrib import messages
from django.core.validators import MinValueValidator, MaxValueValidator




class ProductForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required = True)
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['owner','slug','created']
   

    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop('request')
         # store value of request 
        print(self.request.user)
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        
        status = self.cleaned_data.get('status')
        
        owner = self.cleaned_data.get('owner')

        usermembership = UserMembership.objects.get(user=self.request.user)
        status_count = Product.objects.filter(status='Active').count()
        if usermembership.membership.name == 'Free' and status == "Active" and status_count == 1:
            self._errors['status'] = self.error_class([
                'You can active only one status'])
 
        return self.cleaned_data
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = ProductImages
        fields = ('image', )



class MembershipForm(forms.ModelForm):
    class Meta:
        model = Memberships
        fields = '__all__'


class UserMembershipForm(forms.ModelForm):
    class Meta:
        model = UserMembership
        fields = '__all__'


class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = '__all__'
        exclude = ['bid_product','user','bid_status']



class AcceptBidForm(forms.Form):
    bid_status = forms.CharField(max_length=100)

    


# from django import forms


class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(5),
            MaxValueValidator(50)
        ]
    )    

   
    


