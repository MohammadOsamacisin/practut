from . models import Memberships, UserMembership



def membershiprender(request):
   if request.user.is_authenticated:
      return {
       'memberhsipname': UserMembership.objects.get(user=request.user),
    }
   

   return {}