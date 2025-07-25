from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField( validators=[UniqueValidator(queryset=User.objects.all())]
)
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]

    )
    password = serializers.CharField(write_only=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True)  # ⬅️ Required!

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 're_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if attrs['username'] != attrs['email']:
            raise serializers.ValidationError({"username": "Username and email must be identical."})
        return attrs


    def create(self, validated_data):
        validated_data.pop('re_password')  # don’t store this
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    uid = serializers.CharField()
    token = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # only expose safe fields
        fields = ('id', 'username', 'email', 'date_joined')
