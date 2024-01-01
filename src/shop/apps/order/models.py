from django.db import models
from django.utils.translation import ugettext_lazy as _
from shop.apps.catalog.models import Product

from shop.auths.users.models import User


class Location(models.Model):
    state = models.CharField(_('State'), max_length=256)
    city = models.CharField(_('City'), max_length=256)
    address = models.CharField(_('Address'), max_length=256)

    def __str__(self):
        return self.city + " , " + self.state


class Order(models.Model):
    payment_methods = (('Card', 'Card'), ('Pay On Delivery', 'Pay On Delivery'),
                       ('Bank Transfer', 'Bank Transfer'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(_('payment method'), max_length=250, choices=payment_methods)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
