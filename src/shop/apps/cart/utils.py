from typing import Optional, Union

from shop.apps.cart.cart import Cart
from shop.apps.cart.models import CartModel

from shop.apps.cart.cart import basket_add_item, basket_item_add_quantity, basket_item_minus_quantity, \
    basket_remove_item, clear_basket
from shop.apps.cart.serializers import SessionBasketSerializer, CartItemsSerializer, CartSerializer


class BasketOperationTypes:
    basket_add = 'add'
    item_add_quantity = 'add_quantity'
    item_minus_quantity = 'minus quantity'
    basket_clear = 'clear'


class BasketMixin:
    """
    Mixin which do some operations with
    session basket or with basket from db and
    returns data with information about basket.

    Mixin works with two types of basket:
    Session basket and DB Basket.

    If user is not authenticated, this mixin will be
    working with Session basket, in other case with DB Basket.
    """
    operation_type: Optional[str] = None
    __basket: Union[Cart, CartModel, None] = None

    def _basket_add_item(self, request, product):
        self.reset_basket_option()
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
            self.__basket.add(product)
        else:
            self.__basket, _ = CartModel.objects.prefetch_related('items'). \
                select_related('user').get_or_create(user=request.user)
            basket_add_item(self.__basket, product)

    def _basket_add_item_quantity(self, request, product):
        self.reset_basket_option()
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
            self.__basket.add_quantity(product)
        else:
            self.__basket, _ = CartModel.objects.prefetch_related('items'). \
                select_related('user').get_or_create(user=request.user)
            basket_item_add_quantity(self.__basket, product)

    def _basket_minus_item_quantity(self, request, product):
        self.reset_basket_option()
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
            self.__basket.minus_quantity(product)
        else:
            self.__basket, _ = CartModel.objects.prefetch_related('items'). \
                select_related('user').get_or_create(user=request.user)
            basket_item_minus_quantity(self.__basket, product)

    def _basket_remove_item(self, request, product):
        self.reset_basket_option()
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
            self.__basket.remove(product)
        else:
            self.__basket, _ = CartModel.objects.prefetch_related('items'). \
                select_related('user').get_or_create(user=request.user)
            basket_remove_item(self.__basket, product)

    def _basket_clear(self, request):
        self.reset_basket_option()
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
            self.__basket.clear()
        else:
            self.__basket, _ = CartModel.objects.prefetch_related('items'). \
                select_related('user').get_or_create(user=request.user)
            clear_basket(self.__basket)

    def clear_exist_basket(self, request):
        """
        We are using this method only if user
        is authenticated and use of this method
        is only expected when self.__basket is not
        None and this is Basket model instance.
        For example, we are setting self.__basket
        in method get_basket_data as Basket model
        instance if user is authenticated.

        The main use of this method is to avoid
        needlessly accessing the cart table when
        we are clearing it.
        """
        if request.user.is_authenticated:
            clear_basket(self.__basket)

    @staticmethod
    def get_basket_len(basket):
        return len(basket)

    def get_basket_data(self, request):
        """
        This method checks whether the user is
        authenticated or not, and based on that,
        returns either Session Basket or DB Basket data.

        Args:
            request (Request): The user's request.

        Returns:
            data (dict): dictionary with information about basket.
        """
        self.reset_basket_option()
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
            serializer = SessionBasketSerializer(self.__basket)
            basket_data = serializer.data
            data = {'total_amount': self.__basket.total_amount,
                    'total_quantity_of_products': len(self.__basket)}
            data.update(basket_data)
        else:
            self.__basket, _ = CartModel.objects.prefetch_related('items'). \
                select_related('user').get_or_create(user=request.user)
            items = self.__basket.items.all().select_related('product').distinct()
            items_serializer = CartItemsSerializer(instance=items, many=True)
            basket_data = items_serializer.data
            basket_serializer = CartSerializer(instance=self.__basket)
            data = {'basket': basket_serializer.data,
                    'items': basket_data,
                    'total_amount': self.__basket.total_amount,
                    'total_quantity_of_products': len(self.__basket)}
        return data

    def basket_operation(self, request, product=None):
        """
        This method calls other methods for basket operations
        depending on the specified operation_type.

        Args:
            request (Request): The user's request.
            product (Products): The product on which the operation will be performed.
        """
        self.reset_basket_option()
        if self.operation_type == BasketOperationTypes.basket_add:
            self._basket_add_item(request, product)
        elif self.operation_type == BasketOperationTypes.item_add_quantity:
            self._basket_add_item_quantity(request, product)
        elif self.operation_type == BasketOperationTypes.item_minus_quantity:
            self._basket_minus_item_quantity(request, product)
        elif self.operation_type == BasketOperationTypes.basket_clear:
            self._basket_clear(request)

        return self.get_basket_data(request)

    def basket_items(self, request):
        if not request.user.is_authenticated:
            self.__basket = Cart(request)
        else:
            self.__basket, _ = CartModel.objects.get_or_create(user=request.user)
        for item in self.__basket:
            yield item

    def reset_basket_option(self):
        self.__basket = None
