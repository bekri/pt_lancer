# accounts/urls.py
from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, TestAuthentificationView, PassWordResetConfirm, PasswordResetRequestViews, SetNewPassword, LogoutUserView

urlpatterns =[
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verification/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthentificationView.as_view(), name='granted'),
    path('password-reset/', PasswordResetRequestViews.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PassWordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]