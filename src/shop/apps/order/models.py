from django.db import models
from django.utils.translation import ugettext_lazy as _
from shop.apps.catalog.models import Product

from shop.auths.users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):
    state = models.CharField(_('State'), max_length=256)
    city = models.CharField(_('City'), max_length=256)
    address = models.CharField(_('Address'), max_length=256)

    def __str__(self):
        return self.city + " , " + self.state


class Order(models.Model):
    ORDER_STATUSES = (
        (1, 'New'),
        (2, 'Processing'),
        (3, 'Ready to ship'),
        (4, 'Shipped'),
        (5, 'Delivered'),
        (6, 'Canceled')
    )
    payment_methods = (('Card', 'Card'), ('Pay On Delivery', 'Pay On Delivery'),
                       ('Bank Transfer', 'Bank Transfer'))
    order_status = models.IntegerField(verbose_name='Order status',
                                       choices=ORDER_STATUSES,
                                       default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(_('payment method'), max_length=250, choices=payment_methods)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        else:
            return total



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title + " - " + str(self.quantity)
    @property
    def get_cost(self):
        return self.price * self.quantity

class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code








































