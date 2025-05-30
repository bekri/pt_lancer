from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, PassWordResetConfirm, PasswordResetRequestViews, SetNewPassword, save_location, dashboard,UserProfileUpdateView
from . import views
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verification/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestViews.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PassWordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),  # Corrected URL name
    path('save-location/', save_location, name='save_location'),
]
