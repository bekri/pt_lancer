from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='accounts/signup.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    path('verification/', TemplateView.as_view(template_name='accounts/verify.html'), name='verify'),  # Add this line for the verification page

    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/auth/', include('social_accounts.urls')),
]