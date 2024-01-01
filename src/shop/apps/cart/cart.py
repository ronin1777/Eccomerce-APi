from shop.apps.catalog.models import Product
from typing import NamedTuple, Optional
from django.conf import settings
import copy

from shop.apps.cart.models import CartItems, CartModel

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    @property
    def get_total_Price(self, ):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()


class BasketItemData(NamedTuple):
    item: Optional[CartItems] = None
    exist: Optional[bool] = None


def check_basket_item(basket, product):
    product_id = product.id
    if CartItems.objects.filter(basket=basket, product_id=product_id).exists():
        item = CartItems.objects.get(basket=basket,
                                       product_id=product_id)
        return BasketItemData(item=item, exist=True)
    return BasketItemData(exist=False)


def get_or_create_basket_item(basket, product) -> BasketItemData:
    product_id = product.id
    item_data = check_basket_item(basket, product)
    if item_data.item and item_data.exist:
        item = CartItems.objects.get(basket=basket,
                                       product_id=product_id)
    else:
        item = CartItems.objects.create(basket=basket,
                                          product=product,
                                          quantity=1,
                                          total_price=product.price)
        return BasketItemData(item=item, exist=True)
    return BasketItemData(item, exist=False)


def basket_add_item(basket, product):
    basket_item_data = get_or_create_basket_item(basket, product)
    if basket_item_data.exist:
        basket_item_data.item.quantity = 1
        basket_item_data.item.save()
    else:
        basket_item_data.item.quantity += 1
        basket_item_data.item.save()


def basket_remove_item(basket, product):
    try:
        item = CartItems.objects.get(basket=basket,
                                       product_id=product.id)
        item.delete()
    except CartItems.DoesNotExist:
        return False
    return True


def basket_item_add_quantity(basket, product):
    basket_item_data = check_basket_item(basket, product)
    if basket_item_data.item and basket_item_data.exist:
        basket_item_data.item.quantity += 1
    basket_item_data.item.save()


def basket_item_minus_quantity(basket, product):
    basket_item_data = check_basket_item(basket, product)
    if basket_item_data.item and basket_item_data.exist:
        if basket_item_data.item.quantity > 0:
            basket_item_data.item.quantity -= 1
            basket_item_data.item.save()
        else:
            basket_remove_item(basket, product)


def clear_basket(basket):
    try:
        items = CartItems.objects.filter(basket=basket)
        for item in items:
            item.delete()
        return True
    except CartModel.DoesNotExist:
        return False





















































