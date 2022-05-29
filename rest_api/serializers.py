from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from rest_api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')
        extra_kwargs = {
            "password": {
                'required': False,
                'write_only': True,
            },
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, label='Confirm password'
    )
    class Meta:
        model = User
        fields = ['email', 'full_name', 'user_type', 'password', 'password2']

        extra_kwargs = {
            "email": {
                'required': True,
                'allow_blank': False,
                'validators': [
                    EmailValidator
                ]
            },
            "full_name": {
                'required': True,
                'allow_blank': False,
            },
            "password": {
                'write_only': True
            },
        }

    def create(self, validated_data):
        email = validated_data['email']
        full_name = validated_data['full_name']
        user_type= validated_data['user_type']
        password = validated_data['password']
        password2 = validated_data['password2']
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        if password != password2:
            raise serializers.ValidationError({'password': 'The two passwords differ.'})
        user = User(email=email, full_name=full_name, user_type=user_type)
        user.set_password(password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {'error': {'detail': ['No active account found with the given credentials.']}}
    }

    def validate(self, user_data):
        user_response = super(
            CustomTokenObtainPairSerializer, self).validate(user_data)

        # Access token with to include user detail.
        user_response.pop('refresh')
        user_response.update({
            "user": UserSerializer(self.user).data
        })

        return user_response