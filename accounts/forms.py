from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from product.models import Memberships, UserMembership

class SignUpForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    #birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    # free_membership = Membership.objects.get(membership_type='Free')

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'birth_date','email', 'password1', 'password2', )
        fields = ('username', 'email', 'password1', 'password2', )
    

    # def save(self):
    #   user = super().save(commit=False)
    #   user.save()
    #   # Creating a new UserMembership
    #   user_membership = UserMembership.objects.create(user=user, membership=self.free_membership)
    #   user_membership.save()
    #   # Creating a new UserSubscription
    #   user_subscription = Subscription()
    #   user_subscription.user_membership = user_membership
    #   user_subscription.save()
    #   return user