from django import forms
from .models import Message

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Send a message...',
                'class': 'w-full py-4 px-6 rounded-xl border bg-cyan-950'
            })
        }