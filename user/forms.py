from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='아이디',help_text='')
    password = forms.CharField(label='비밀번호',widget=forms.PasswordInput())
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ['username', 'password', 'email']