from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from . tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from product.models import Memberships, UserMembership
from . forms import SignUpForm



def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            membership = Memberships.objects.get(slug='free')
            # import pdb;
            # pdb.set_trace()
            usermembership = UserMembership.objects.create(user=user,membership=membership)
            current_site = get_current_site(request)
            subject = 'Activate Your My ReselAccount'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            
            # user.email_user(subject, message,settings.EMAIL_HOST_USER)
            send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    # fail_silently=False,
                    )
            return redirect('accounts:account_activation_sent')
        else:
            return render(request,'registration/sign_up.html',context={"form": form})
    return render(request,'registration/sign_up.html',context={"form": SignUpForm()})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('accounts:login')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


@login_required
def home(request):
    
    return render(request, 'registration/home.html')