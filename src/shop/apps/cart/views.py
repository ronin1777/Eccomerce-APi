from shop.apps.cart.cart import Cart

from shop.apps.cart.models import CartModel, CartItems

def get_or_create_basket(request, user):
    """
    This function is used to get the basket from
    the session and create it in the database.
    """
    basket = Cart(request)
    user_basket, _ = CartModel.objects.get_or_create(user=user)
    for item in basket:
        CartItems.objects.get_or_create(basket=user_basket,
                                          product=item['product'],
                                          quantity=item['quantity'],
                                          total_price=item['total_price'])
    basket.clear()


