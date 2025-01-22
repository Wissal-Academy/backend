from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validate_data):
        user = User.objects.create(
            username=validate_data['username'],
            email=validate_data['email'],
        )
        user.set_password(validate_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        # check if the username and password are not empty
        # USERNAME , PASJABISJAGB
        if username and password:
            # Get the first object
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    "username": user.username,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }
            else:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("The username and password should not be empty")


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
