from django.conf.locale import fr
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.auths.users.models import User, Profile

from django.core.mail import send_mail
from .models import User
from ...envs import common


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Website'
        message = f'Hello {instance.username},\n\nWelcome to our website! Thank you for joining us.'
        from_email = common.EMAIL_HOST_USER
        recipient_list = [instance.username]
        send_mail(subject, message, from_email, recipient_list)

