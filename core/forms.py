from django import forms

from .models import Contact

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border bg-cyan-950'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('full_name', 'email', 'subject', 'message')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Full Name*',
                'class': INPUT_CLASSES
            }),

            'email': forms.TextInput(attrs={
                'placeholder': 'Email Address*',
                'class': INPUT_CLASSES
            }),

            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject*',
                'class': INPUT_CLASSES
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Send a message...',
                'class': INPUT_CLASSES
            }),
        }