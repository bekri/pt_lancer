#accounts views.py
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, LoginSerializer, SetNewPasswordSerializer, PasswordResetRequestSerializer, LogoutUserSerializer, VerifyEmailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import send_code_to_user
from .models import OneTimePassword, User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages

# Create your views here.


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request):
        user_data = request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])
            # Use settings to determine the protocol
            protocol = 'https://' if settings.SECURE_SSL_REDIRECT else 'http://'
            return redirect(f'{protocol}{request.get_host()}/verification')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyUserEmail(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data['otp']
        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                # Add a success message using Django's messages framework
                messages.success(request, 'Email verified successfully! You can now access your account.')
                # Redirect to the login page
                return redirect('/login')
            else:
                return Response({
                    'message': 'User already verified'
                }, status=status.HTTP_200_OK)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'Invalid passcode'
            }, status=status.HTTP_404_NOT_FOUND)

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Check if the user's email is verified
            if user.is_verified:  # Assuming 'is_verified' is the attribute for email verification
                login(request, user)  # Log the user in
                # Redirect to the dashboard URL
                return redirect('/dashboard/')  # Adjust this to match your dashboard URL
            else:
                return Response({'error': 'Email is not verified.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class Dashboard(GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/dashboard.html')

    
class PasswordResetRequestViews(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'data': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':"a link has been sent to your email address, to reset your password!"}, status=status.HTTP_200_OK)
    

class PassWordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'The reset link is invalid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success':True,'message': 'The reset link is valid, please reset your password'}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError: 
            return Response ({'message': 'The reset link is invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'Your password has been successfully reset. 😊'}, status=status.HTTP_200_OK)
    

class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)





            
