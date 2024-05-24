#accounts/manager.py
from typing import Any
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager): 
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Please enter a valid email address"))

    def create_user(self, email, first_name, last_name, password, role, **extra_fields):
         # Validate email
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        validate_email(email)

        # Validate names
        if not first_name:
            raise ValueError(_("The first name must be set"))
        if not last_name:
            raise ValueError(_("The last name must be set"))

        # Validate role
        if role not in ('trainer', 'client'):
            raise ValueError(_("The role must be either 'trainer' or 'client'"))

        # Validate password
        if password is not None:
            validate_password(password)
        else:
            raise ValueError(_("A password must be provided"))

        # Create the user object
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        user = self.create_user(
            email, first_name, last_name, password, 'trainer', **extra_fields  # Default role for superuser is 'trainer'
        )
        user.save(using=self._db)
        return user
