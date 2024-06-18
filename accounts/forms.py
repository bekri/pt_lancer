# accounts/forms.py
from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'role', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),  # Accept only image files
        }


class LocationForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
