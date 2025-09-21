from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'class': 'register-input'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First name',
            'class': 'register-input'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last name',
            'class': 'register-input'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'your@email.com',
            'class': 'register-input'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'class': 'register-input'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'class': 'register-input'
        })

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
            'class': ''
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter your password',
            'class': ''
        })
