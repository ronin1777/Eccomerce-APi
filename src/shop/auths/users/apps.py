from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop.auths.users'

    def ready(self):
        import shop.auths.users.signals


