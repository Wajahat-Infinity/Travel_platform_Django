from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from src.accounts.models import User


class BuyerPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
