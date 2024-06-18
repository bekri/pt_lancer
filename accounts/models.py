from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Auth Dictionary
AUTH_PROVIDERS = {'email': 'email', 'google': 'google', 'facebook': 'facebook'}

# Define the custom upload path function
def user_profile_picture_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    return 'profile_pictures/user_{0}/{1}'.format(instance.id, filename)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    phone = models.CharField(max_length=255, verbose_name=_("Phone Number"))
    role = models.CharField(max_length=255, choices=[
        ('trainer', _('Trainer')),
        ('client', _('Client')),
    ], verbose_name=_("Role"))

    profile_picture = models.ImageField(upload_to=user_profile_picture_upload_path, default='default_avatar.png')
    

    # Remove the address field and keep longitude, latitude, city, and country fields
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    #Admin Dashboard stuff
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff status"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Superuser status"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Verified"))
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_token(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, default="")

    def __str__(self):
        return f"{self.user.first_name}- passcode"