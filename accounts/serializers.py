#accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes, force_str  
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, Token





class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2=serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields=['email', 'phone', 'first_name', 'last_name', 'password', 'password2', 'role']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token', 'role']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        tokens = user.get_token()
        return {
            'email': user.email,
            'full_name': user.get_full_name,  # Fixed here
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh'],
            'user': user,
        }


class PasswordResetRequestSerializer(serializers.Serializer):

    email=serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f'Hey {user.first_name}, \n Use the link below to reset your password \n {abslink}'
            data={
                'email_body': email_body,
                'email_subject':"{site_domain} Password reset",
                'to_email':user.email,
            }
            send_normal_email()


        return super().validate(attrs)
    

class  SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=['password', 'confirm_password', 'uidb64', 'token']
    
    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id= force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid or has expired', 401)
            if password!=confirm_password:
                raise AuthenticationFailed('Passwords do not match')
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed('Link is invalid or expired')
        
class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_messages = {
        'bad_token':('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token=attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        
class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        fields = ['otp']
