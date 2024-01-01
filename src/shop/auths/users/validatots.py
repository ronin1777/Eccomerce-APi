from django.core.validators import RegexValidator


class IranianMobileNumberValidator(RegexValidator):
    regex = r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$"
    message = "Please enter a valid Iranian mobile number."
