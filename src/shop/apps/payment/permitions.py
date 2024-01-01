from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from shop.apps.order.models import Order


class IsPaymentByUser(BaseException):
    """
    Check if payment belongs to the appropriate buyer or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user or request.user.is_staff




