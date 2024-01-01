from django.db import models
from django.utils.translation import ugettext_lazy as _



class Location(models.Model):
    state = models.CharField(_('State'), max_length=256)
    city = models.CharField(_('City'), max_length=256)
    address = models.CharField(_('Address'), max_length=256)

    def __str__(self):
        return self.city + " , " + self.state