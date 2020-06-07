from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets={
            'username': TextInput(attrs={'class':'input','placholder':'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placholder': 'email'}),
            'username': TextInput(attrs={'class': 'input', 'placholder': 'first_name'}),
            'username': TextInput(attrs={'class': 'input', 'placholder': 'last_name'}),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Bursa', 'Bursa'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class':'input','placholder':'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placholder': 'address'}),
            'city': Select(attrs={'class': 'input', 'placholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placholder': 'country'}),
            'image': FileInput(attrs={'class': 'input', 'placholder': 'image'}),
        }