from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms


class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl text-black'
    }))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={
        'placeholder': 'New password',
        'class': 'w-full py-4 px-6 rounded-xl text-black'
    }))

    new_password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput(attrs={
        'placeholder': 'New password confirmation',
        'class': 'w-full py-4 px-6 rounded-xl text-black'
    }))


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl bg-cyan-900'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl bg-cyan-900'
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl bg-cyan-900'
    }))

#    first_name = forms.CharField(widget=forms.TextInput(attrs={
#        'placeholder': 'Your first name',
#        'class': 'w-full py-4 px-6 rounded-xl'
#    }))

#    last_name = forms.CharField(widget=forms.TextInput(attrs={
#        'placeholder': 'Your last name',
#        'class': 'w-full py-4 px-6 rounded-xl'
#    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl bg-cyan-900'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl bg-cyan-900'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl bg-cyan-900'
    }))