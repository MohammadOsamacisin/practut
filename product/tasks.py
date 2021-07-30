import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery.schedules import crontab
from celery.decorators import periodic_task
from product.models import Memberships, UserMembership
from django.db.models.signals import post_save
from django.dispatch import receiver


from celery import shared_task

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)


# @receiver(post_save, sender=User)
# def update_random_user_accounts(sender, instance, created, **kwargs):
#     if created:
#         User.objects.create()
#         usermembership = UserMembership.objects.create(user=user,membership=membership)
#     try:
#         instance.profile.save()
#     except ObjectDoesNotExist:
#         Profile.objects.create(user=instance)






@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="something",
    ignore_result=True
)
def something():
    print("Hello")