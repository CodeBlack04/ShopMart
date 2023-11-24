from django.urls import path, include, reverse_lazy

from django.contrib.auth import views as auth_views
from . import views

from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm

app_name = 'myauth'

urlpatterns = [
    path('signup/', views.signup, name='signup'),

    path('login/', auth_views.LoginView.as_view(
        template_name='myauth/login.html',
        authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='myauth/password_reset.html',
        email_template_name='myauth/password_reset_email.html',
        form_class=MyPasswordResetForm,
        success_url= reverse_lazy('myauth:password_reset_done')), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='myauth/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myauth/password_reset_confirm.html',
        form_class=MySetPasswordForm,
        success_url = reverse_lazy('myauth:password_reset_complete')), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='myauth/password_reset_complete.html'), name='password_reset_complete'),
]