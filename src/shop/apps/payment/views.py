from rest_framework.viewsets import ModelViewSet

from shop.apps.payment.models import Payment
from django.shortcuts import get_object_or_404

from shop.apps.payment.serializers import PaymentSerializer
from rest_framework.generics import RetrieveUpdateAPIView

from shop.apps.order.models import Order
from shop.apps.payment.serializers import CheckoutSerializer
from rest_framework.views import APIView


class PaymentViewSet(ModelViewSet):
    """
    CRUD payment for an order
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(order__user=user)


class CheckoutAPIView(RetrieveUpdateAPIView):


    queryset = Order.objects.all()
    serializer_class = CheckoutSerializer


class StripeCheckoutSessionCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))

        order_items = []

        for order_item in order.items.all():
            product = order_item.product
            quantity = order_item.quantity

            data = {
                "price_data": {
                    "currency": "toman",
                    "unit_amount_decimal": product.price,
                    "product_data": {
                        "name": product.title,
                        "description": product.description,
                    },
                },
                "quantity": quantity,
            }

            order_items.append(data)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=order_items,
            metadata={"order_id": order.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )

        return Response(
            {"sessionId": checkout_session["id"]}, status=status.HTTP_201_CREATED
        )


class StripeWebhookAPIView(APIView):
    """
    Stripe webhook API view to handle checkout session completed and other events.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            order_id = session["metadata"]["order_id"]

            print("Payment successfull")

            payment = get_object_or_404(Payment, order=order_id)
            payment.status = "C"
            payment.save()

            order = get_object_or_404(Order, id=order_id)
            order.status = "C"
            order.save()

            # TODO - Decrease product quantity

            send_payment_success_email_task.delay(customer_email)

        # Can handle other events here.

        return Response(status=status.HTTP_200_OK)
