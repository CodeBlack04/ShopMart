from django.shortcuts import render, redirect
from django.contrib import messages

from verify_email.email_handler import send_verification_email

from .forms import SignupForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            inactive_user = send_verification_email(request, form=form)

            messages.success(request, 'Please check your email to activate your account!')
            
            return redirect('/')
        
    else:
        form = SignupForm()

    return render(request=request, template_name='myauth/signup.html', context={
        'title': 'SignUp',
        'form': form,
    })

