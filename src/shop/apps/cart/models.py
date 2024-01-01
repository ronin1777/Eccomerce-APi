from django.db import models

from shop.auths.users.models import User


class CartModel(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                blank=True,
                                null=True,
                                related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created at')

    class Meta:
        verbose_name = 'basket'
        verbose_name_plural = 'Baskets'

    def __str__(self):
        return f'Basket of {self.user.username}'

    def __len__(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())