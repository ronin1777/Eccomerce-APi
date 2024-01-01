from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, Token
from shop.auths.users.models import User, Profile

import logging


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8
       , max_length=68, write_only=True)

    def handle_error(self, data):
        errors = self.context['errors']
        if errors:
            data['errors'] = errors
        return super().handle_error(data)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LogInSerializer(TokenObtainPairSerializer):
    # def get_tokens(self, user):
    #     token = Token.for_user(user)
    #     refresh = RefreshToken.for_user(user)
    #     access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    #     token.set_exp(access_token_lifetime)
    #     return {
    #         'access': str(token),
    #         'refresh': str(refresh)
    #     }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = RegisterSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {"bad_token": "Token is invalid or expired"}

    def validate(self, data):
        self.token = data["refresh"]
        return data

    # def save(self, **kwargs):
    #     try:
    #         RefreshToken(self.token).blacklist()
    #     except TokenError as e:
    #         raise ValidationError({"refresh": [str(e)]})
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception as e:
            # Log the exception for debugging purposes
            logging.error(f"Failed to blacklist token: {e}")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'user', 'age', 'first_name', 'last_name', 'phon_number', 'birthday', 'bio', 'address', 'balance', 'gender']
        read_only_fields = ['balance', 'user', 'user_id']














































































